import json
from tinydb import TinyDB, Query
from datetime import datetime, date
import uuid

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class DatabaseConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.device_db_file = 'devices.json'
        self.user_db_file = 'users.json'
        self.device_db = TinyDB(self.device_db_file)
        self.user_db = TinyDB(self.user_db_file)

    def get_devices_table(self):
        return self.device_db.table('devices')  # Name der Gerätetabelle

    def get_users_table(self):
        return self.user_db.table('users')  # Name der Benutzertabelle

class UserDatabase(DatabaseConnector):
    def __init__(self):
        super().__init__()

    def add_user(self, username, email, role):
        if self.user_db.search(Query().username == username):
            return "Benutzer existiert bereits."

        user_id = str(uuid.uuid4())

        user_data = {"user_id": user_id, "username": username, "email": email, "role": role}
        self.user_db.insert(user_data)
        return f"Nutzer '{username}' erfolgreich angelegt mit der Benutzer-ID '{user_id}' als {role} mit der E-Mail '{email}'."

    def get_user_by_name_and_email(self, name, email):
        return self.user_db.get((Query().username == name) & (Query().email == email))

    def get_all_users(self):
        return self.user_db.all()

class DeviceDatabase(DatabaseConnector):
    def __init__(self):
        super().__init__()

    def add_device(self, device_id, device_name, device_type, device_description, responsible_person, end_of_life=None):
        if self.device_db.search(Query().device_id == device_id):
            return f"Gerät mit ID '{device_id}' existiert bereits."

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        device_data = {
            "device_id": device_id,
            "device_name": device_name,
            "device_type": device_type,
            "device_description": device_description,
            "responsible_person": responsible_person,
            "end_of_life": end_of_life.isoformat() if end_of_life else None,
            "__last_update": current_time,
            "__creation_date": current_time
        }
        self.device_db.insert(device_data)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich angelegt als '{device_type}' mit der Beschreibung '{device_description}'."

    def modify_device(self, device_id, device_name, device_type, device_description, end_of_life=None):
        Device = Query()
        if not self.device_db.contains(Device.device_id == device_id):
            return f"Gerät mit ID '{device_id}' existiert nicht."

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_data = {
            'device_name': device_name,
            'device_type': device_type,
            'device_description': device_description,
            'end_of_life': end_of_life.isoformat() if end_of_life else None,
            '__last_update': current_time
        }
        self.device_db.update(update_data, Device.device_id == device_id)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich aktualisiert als '{device_type}' mit der Beschreibung '{device_description}'."

    def get_all_devices(self):
        return self.device_db.all()