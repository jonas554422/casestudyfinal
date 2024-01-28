import json
from tinydb import TinyDB, Query
from datetime import datetime, date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date to ISO format
        return super().default(obj)


class UserDatabase:
    def __init__(self, user_db_file='users.json'):
        self.user_db = TinyDB(user_db_file)

    def add_user(self, username, email, role):
        # Überprüfe, ob der Benutzer bereits existiert
        if self.user_db.search(Query().username == username):
            return "Benutzer existiert bereits."

        # Füge den neuen Benutzer zur Datenbank hinzu
        user_data = {"username": username, "email": email, "role": role}
        self.user_db.insert(user_data)
        return f"Nutzer '{username}' erfolgreich angelegt als {role} mit der E-Mail '{email}'."

    def get_user_by_name_and_email(self, name, email):
        return self.user_db.get((Query().username == name) & (Query().email == email))


class DeviceDatabase:
    def __init__(self, device_db_file='devices.json'):
        self.device_db = TinyDB(device_db_file)

    def add_device(self, device_id, device_name, device_type, device_description, responsible_person, first_maintenance, end_of_life=None):
        # Überprüfe, ob das Gerät bereits existiert
        if self.device_db.search(Query().device_id == device_id):
            return f"Gerät mit ID '{device_id}' existiert bereits."

        # Füge das neue Gerät zur Datenbank hinzu
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        device_data = {
            "device_id": device_id,
            "device_name": device_name,
            "device_type": device_type,
            "device_description": device_description,
            "responsible_person": responsible_person,
            "end_of_life": end_of_life.isoformat() if end_of_life else None,
            "__last_update": current_time,
            "__creation_date": current_time,
            "first_maintenance": first_maintenance.isoformat() if first_maintenance else None
            #"next_maintenance": next_maintenance,
            #"__maintenance_interval": __maintenance_interval,
            #"__maintenance_cost": __maintenance_cost
        }
        self.device_db.insert(device_data)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich angelegt als '{device_type}' mit der Beschreibung '{device_description}'."

    def modify_device(self, device_id, device_name, device_type, device_description, next_maintenance, __maintenance_interval, __maintenance_cost, end_of_life=None):
        # Überprüfe, ob das Gerät existiert
        Device = Query()
        if not self.device_db.contains(Device.device_id == device_id):
            return f"Gerät mit ID '{device_id}' existiert nicht."

        # Aktualisiere das Gerät in der Datenbank
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_data = {
            'device_name': device_name,
            'device_type': device_type,
            'device_description': device_description,
            'end_of_life': end_of_life.isoformat() if end_of_life else None,
            '__last_update': current_time,
            'next_maintenance': next_maintenance,
            '__maintenance_interval': __maintenance_interval,
            '__maintenance_cost': __maintenance_cost
        }
        self.device_db.update(update_data, Device.device_id == device_id)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich aktualisiert als '{device_type}' mit der Beschreibung '{device_description}'."

    def get_all_devices(self):
        return self.device_db.all()