import json
from tinydb import TinyDB, Query

class DeviceDatabase:
    def __init__(self, user_db_file='users.json', device_db_file='devices.json'):
        self.user_db = TinyDB(user_db_file)
        self.device_db = TinyDB(device_db_file)

    # Restlicher Code bleibt unverändert

    def add_user(self, username, email, role):
        # Überprüfe, ob der Benutzer bereits existiert
        if self.user_db.search(Query().username == username):
            return "Benutzer existiert bereits."

        # Füge den neuen Benutzer zur Datenbank hinzu
        user_data = {"username": username, "email": email, "role": role}
        self.user_db.insert(user_data)
        return f"Nutzer '{username}' erfolgreich angelegt als {role} mit der E-Mail '{email}'."

    def add_device(self, device_name, device_type, device_description):
        # Überprüfe, ob das Gerät bereits existiert
        if self.device_db.search(Query().device_name == device_name):
            return f"Gerät '{device_name}' existiert bereits."

        # Füge das neue Gerät zur Datenbank hinzu
        device_data = {
            "device_name": device_name,
            "device_type": device_type,
            "device_description": device_description
        }
        self.device_db.insert(device_data)
        return f"Gerät '{device_name}' erfolgreich angelegt als '{device_type}' mit der Beschreibung '{device_description}'."
