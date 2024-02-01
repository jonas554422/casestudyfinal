import streamlit as st
from backend import UserDatabase, DeviceDatabase, ReservationDatabase
from tinydb import Query

def create_new_user():
    st.title("Nutzer anlegen")
    username = st.text_input("Benutzername")
    email = st.text_input("E-Mail")
    role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])
    submitted = st.button("Nutzer anlegen")
    if submitted:
        user_db = UserDatabase()
        result = user_db.add_user(username, email, role)
        st.success(result)

def create_or_modify_device():
    st.title("Gerät anlegen")
    device_id = st.number_input("ID/ Inventarnummer", step=1, value=0)
    device_name = st.text_input("Gerätename")
    device_type = st.selectbox("Gerätetyp", ["Typ A", "Typ B", "Typ C"])
    device_description = st.text_area("Beschreibung")
    responsible_person_name = st.text_input("Name des verantwortlichen Benutzers")
    responsible_person_email = st.text_input("E-Mail des verantwortlichen Benutzers")
    end_of_life = st.date_input("End of Life Datum (optional)", value=None)
    end_of_life = end_of_life if end_of_life else None
    first_maintenance = st.date_input("Datum der ersten Wartung")
    next_maintenance = st.date_input("Datum der nächsten Wartung")
    __maintenance_interval = st.number_input("Wartungsinterval in Tagen")
    __maintenace_coast = st.number_input("Kosten/€ pro Wartung")
    submitted = st.button("Gerät speichern")
    if submitted:
        user_db = UserDatabase()
        device_id = int(device_id) if device_id else 0
        responsible_person = user_db.get_user_by_name_and_email(responsible_person_name, responsible_person_email)
        if responsible_person and responsible_person['role'] == 'Geräteverantwortlicher':
            device_db = DeviceDatabase()
            result = device_db.add_device(device_id, device_name, device_type, device_description, responsible_person, end_of_life, first_maintenance, next_maintenance, __maintenance_interval, __maintenace_coast)
            st.success(result)
        else:
            st.error("Nutzer ist nicht als Geräteverantwortlicher registriert.")

def modify_device():
    st.title("Gerät ändern")
    devices_db = DeviceDatabase()
    devices = devices_db.get_all_devices()

    if devices:
        device_options = {device['device_id']: device for device in devices}
        device_option_ids = list(device_options.keys())
        selected_device_id = st.selectbox("Gerät auswählen", device_option_ids, format_func=lambda x: device_options[x]['device_name'])
        selected_device = device_options[selected_device_id]
        
        device_name = st.text_input("Neuer Gerätename", value=selected_device['device_name'])
        device_type = st.selectbox("Neuer Gerätetyp", ["Typ A", "Typ B", "Typ C"], index=["Typ A", "Typ B", "Typ C"].index(selected_device['device_type']))
        device_description = st.text_area("Neue Beschreibung", value=selected_device['device_description'])
        
        if st.button("Änderungen speichern"):
            result = devices_db.modify_device(selected_device['device_id'], device_name, device_type, device_description)
            st.success(result)
    else:
        st.write("Keine Geräte zum Ändern vorhanden.")


def create_or_remove_reservation():
    st.title("Reservierung anlegen oder entfernen")
    devices_db = DeviceDatabase()
    users_db = UserDatabase()
    reservations_db = ReservationDatabase()

    devices = devices_db.get_all_devices()
    users = users_db.get_all_users()

    # Erstelle ein Dictionary mit Geräte-ID als Schlüssel und dem Gerätenamen als Wert
    # Fallback auf 'Unbekanntes Gerät', falls 'device_name' nicht vorhanden ist
    device_options = {device['device_id']: device.get('device_name', 'Unbekanntes Gerät') for device in devices}
    
    selected_device_id = st.selectbox("Gerät auswählen", list(device_options.keys()), format_func=lambda x: device_options[x])
    
    # Erstelle ein Dictionary mit Benutzer-ID als Schlüssel und dem Benutzernamen als Wert
    user_options = {user['user_id']: user['username'] for user in users}
    selected_user_id = st.selectbox("Nutzer auswählen", list(user_options.keys()), format_func=lambda x: user_options[x])

    start_date = st.date_input("Startdatum")
    end_date = st.date_input("Enddatum")

    if st.button("Reservierung anlegen"):
        result = reservations_db.add_reservation(selected_device_id, selected_user_id, start_date, end_date)
        st.success(result)

    if st.button("Reservierung entfernen"):
        result = reservations_db.remove_reservation(selected_device_id, selected_user_id, start_date, end_date)
        st.success(result)

    st.subheader("Aktuelle Reservierungen:")
    current_reservations = reservations_db.get_current_reservations_with_details()
    for res in current_reservations:
        st.write(f"Gerät: {res['device_name']}, Nutzer: {res['user_name']}, Zeitraum: {res['start_date']} bis {res['end_date']}")



def main():
    st.title("Geräte-Verwaltung")
    action = st.sidebar.selectbox("Aktion auswählen", ["Nutzer anlegen", "Geräte anlegen", "Geräte ändern", "Reservierung anlegen/entfernen"])
    if action == "Nutzer anlegen":
        create_new_user()
    elif action == "Geräte anlegen":
        create_or_modify_device()
    elif action == "Geräte ändern":
        modify_device()
    elif action == "Reservierung anlegen/entfernen":
        create_or_remove_reservation()

if __name__ == "__main__":
    main()