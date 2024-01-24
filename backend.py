import json
from tinydb import TinyDB, Query

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

    # Aktualisierte Methode, um responsible_person zu akzeptieren
    def add_device(self, device_id, device_name, device_type, device_description, responsible_person):
        # Überprüfe, ob das Gerät bereits existiert
        if self.device_db.search(Query().device_id == device_id):
            return f"Gerät mit ID '{device_id}' existiert bereits."

        # Füge das neue Gerät zur Datenbank hinzu
        device_data = {
            "device_id": device_id,
            "device_name": device_name,
            "device_type": device_type,
            "device_description": device_description,
            "responsible_person": responsible_person  # Hinzugefügt
        }
        self.device_db.insert(device_data)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich angelegt als '{device_type}' mit der Beschreibung '{device_description}'."
    
    def modify_device(self, device_id, device_name, device_type, device_description):
        # Überprüfe, ob das Gerät existiert
        Device = Query()
        if not self.device_db.contains(Device.device_id == device_id):
            return f"Gerät mit ID '{device_id}' existiert nicht."

        # Aktualisiere das Gerät in der Datenbank
        self.device_db.update({'device_name': device_name, 'device_type': device_type, 'device_description': device_description}, Device.device_id == device_id)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich aktualisiert als '{device_type}' mit der Beschreibung '{device_description}'."
    
    def get_all_devices(self):
        return self.device_db.all()
