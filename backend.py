import json
from tinydb import TinyDB, Query
from datetime import datetime, date
import uuid  # Hinzugefügt: Importiere die uuid-Bibliothek


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date to ISO format
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
        return self.device_db.table()

    def get_users_table(self):
        return self.user_db.table()

class UserDatabase(DatabaseConnector):
    def __init__(self):
        super().__init__()

    def add_user(self, username, email, role):
        # Überprüfe, ob der Benutzer bereits existiert
        if self.user_db.search(Query().username == username):
            return "Benutzer existiert bereits."

        # Generiere eine eindeutige Benutzer-ID
        user_id = str(uuid.uuid4())

        # Füge den neuen Benutzer zur Datenbank hinzu
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
            "__creation_date": current_time
        }
        self.device_db.insert(device_data)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich angelegt als '{device_type}' mit der Beschreibung '{device_description}'."

    def modify_device(self, device_id, device_name, device_type, device_description, end_of_life=None):
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
            '__last_update': current_time
        }
        self.device_db.update(update_data, Device.device_id == device_id)
        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich aktualisiert als '{device_type}' mit der Beschreibung '{device_description}'."

    def get_all_devices(self):
        return self.device_db.all()

# Serializer-Klassen
class DeviceSerializer:
    @staticmethod
    def serialize(device_data):
        return json.dumps(device_data, cls=DateEncoder)

class UserSerializer:
    @staticmethod
    def serialize(user_data):
        return json.dumps(user_data, cls=DateEncoder)


class ReservationDatabase(DatabaseConnector):
    def __init__(self):
        super().__init__()

    def add_reservation(self, device_id, user_id, start_date, end_date):
        # Überprüfe, ob die Reservierung bereits existiert
        existing_reservation = self.device_db.search(
            (Query().device_id == device_id) &
            (Query().user_id == user_id) &
            (Query().end_date >= str(start_date)) &
            (Query().start_date <= str(end_date))
        )

        if existing_reservation:
            return "Reservierung für dieses Gerät und diesen Nutzer im angegebenen Zeitraum existiert bereits."

        # Füge die neue Reservierung zur Datenbank hinzu
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reservation_data = {
            "device_id": device_id,
            "user_id": user_id,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "__creation_date": current_time
        }
        self.device_db.insert(reservation_data)
        return f"Reservierung für Gerät ID '{device_id}' und Nutzer ID '{user_id}' erfolgreich angelegt."

    def remove_reservation(self, device_id, user_id, start_date, end_date):
        # Überprüfe, ob die Reservierung existiert
        existing_reservation = self.device_db.search(
            (Query().device_id == device_id) &
            (Query().user_id == user_id) &
            (Query().start_date == str(start_date)) &
            (Query().end_date == str(end_date))
        )

        if not existing_reservation:
            return "Keine Reservierung für dieses Gerät und diesen Nutzer im angegebenen Zeitraum gefunden."

        # Entferne die Reservierung aus der Datenbank
        self.device_db.remove(
            (Query().device_id == device_id) &
            (Query().user_id == user_id) &
            (Query().start_date == str(start_date)) &
            (Query().end_date == str(end_date))
        )

        return f"Reservierung für Gerät ID '{device_id}' und Nutzer ID '{user_id}' erfolgreich entfernt."

