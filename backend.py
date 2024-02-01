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

    def add_device(self, device_id, device_name, device_type, device_description, responsible_person, first_maintenance, next_maintenance, __maintenance_interval, __maintenace_coast, end_of_life=None):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sicherstellen, dass die Datumsfelder korrekt sind
        first_maintenance = first_maintenance.isoformat() if isinstance(first_maintenance, date) else None
        next_maintenance = next_maintenance.isoformat() if isinstance(next_maintenance, date) else None
        end_of_life = end_of_life.isoformat() if isinstance(end_of_life, date) else None


        device_data = {
        "device_id": device_id,
        # restliche Felder
        "end_of_life": end_of_life,
        "__last_update": current_time,
        "__creation_date": current_time,
        "first_maintenance": first_maintenance,
        "next_maintenance": next_maintenance,
        "__maintenance_interval": __maintenance_interval,
        "__maintenance_coast": __maintenace_coast
    }
        self.device_db.insert(json.loads(json.dumps(device_data, cls=DateEncoder)))

        return f"Gerät '{device_name}' mit ID '{device_id}' erfolgreich angelegt als '{device_type}' mit der Beschreibung '{device_description}'."

    def modify_device(self, device_id, device_name, device_type, device_description, end_of_life):
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

class ReservationDatabase(DatabaseConnector):
    def __init__(self):
        super().__init__()
        self.reservation_db = self.device_db.table("reservations")

    def add_reservation(self, device_id, user_id, start_date, end_date):
        if self.reservation_db.search(
            (Query().device_id == device_id) &
            (Query().user_id == user_id) &
            (Query().end_date >= str(start_date)) &
            (Query().start_date <= str(end_date))
        ):
            return "Reservierung für dieses Gerät und diesen Nutzer im angegebenen Zeitraum existiert bereits."

        device = self.device_db.get(Query().device_id == device_id)
        if not device:
            return f"Gerät mit ID '{device_id}' nicht gefunden."
        device_name = device.get('device_name', 'Unknown Device')

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reservation_data = {
            "device_id": device_id,
            "device_name": device_name,
            "user_id": user_id,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "__creation_date": current_time
        }
        self.reservation_db.insert(reservation_data)
        return f"Reservierung für Gerät '{device_name}' (ID: {device_id}) und Nutzer ID '{user_id}' erfolgreich angelegt."

    def remove_reservation(self, device_id, user_id, start_date, end_date):
        if not self.reservation_db.search(
            (Query().device_id == device_id) &
            (Query().user_id == user_id) &
            (Query().start_date == str(start_date)) &
            (Query().end_date == str(end_date))
        ):
            return "Keine Reservierung für dieses Gerät und diesen Nutzer im angegebenen Zeitraum gefunden."

        self.reservation_db.remove(
            (Query().device_id == device_id) &
            (Query().user_id == user_id) &
            (Query().start_date == str(start_date)) &
            (Query().end_date == str(end_date))
        )
        return f"Reservierung für Gerät ID '{device_id}' und Nutzer ID '{user_id}' erfolgreich entfernt."
    
    def get_current_reservations(self):
        current_date = datetime.now().date()
        current_reservations = self.reservation_db.search(
            (Query().start_date <= str(current_date)) &
            (Query().end_date >= str(current_date))
        )
        return current_reservations
    
    def get_current_reservations_with_details(self):
        current_date = datetime.now().date()
        current_reservations = self.reservation_db.search(
            (Query().start_date <= str(current_date)) &
            (Query().end_date >= str(current_date))
        )

        detailed_reservations = []
        for res in current_reservations:
            device = self.device_db.get(Query().device_id == res['device_id'])
            user = self.user_db.get(Query().user_id == res['user_id'])

            detailed_reservations.append({
                'device_name': device['device_name'] if device else 'Unbekanntes Gerät',
                'user_name': user['username'] if user else 'Unbekannter Nutzer',
                'start_date': res['start_date'],
                'end_date': res['end_date']
            })

        return detailed_reservations

class DeviceSerializer:
    @staticmethod
    def serialize(device_data):
        return json.dumps(device_data, cls=DateEncoder)

class UserSerializer:
    @staticmethod
    def serialize(user_data):
        return json.dumps(user_data, cls=DateEncoder)