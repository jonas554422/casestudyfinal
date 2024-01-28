import streamlit as st
from backend import UserDatabase, DeviceDatabase  # Updated import statements
from backend import ReservationDatabase


def create_new_user():
    st.title("Nutzer anlegen")
    username = st.text_input("Benutzername")
    email = st.text_input("E-Mail")
    role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])
    
    submitted = st.button("Nutzer anlegen")
    
    if submitted:
        user_db = UserDatabase()  # Instanziere die UserDatabase-Klasse
        result = user_db.add_user(username, email, role)
        st.success(result)

def create_or_modify_device():
    st.title("Gerät anlegen")
    device_id = st.number_input("ID/ Inventarnummer", step=1, value=0)
    device_name = st.text_input("Gerätename")
    device_type = st.selectbox("Gerätetyp", ["Typ A", "Typ B", "Typ C"])
    device_description = st.text_area("Beschreibung")

    # Hinzugefügt: Informationen über den verantwortlichen Benutzer und End of Life Datum
    responsible_person_name = st.text_input("Name des verantwortlichen Benutzers")
    responsible_person_email = st.text_input("E-Mail des verantwortlichen Benutzers")
    end_of_life = st.date_input("End of Life Datum (optional)")

    submitted = st.button("Gerät speichern")
    
    if submitted:
        user_db = UserDatabase()  # Instanziere die UserDatabase-Klasse
        # Überprüfen Sie, ob device_id leer ist, und verwenden Sie 0 als Dummy-Wert
        device_id = int(device_id) if device_id else 0

        # Überprüfen Sie, ob der verantwortliche Benutzer als Geräteverantwortlicher registriert ist
        responsible_person = user_db.get_user_by_name_and_email(responsible_person_name, responsible_person_email)
        if responsible_person and responsible_person['role'] == 'Geräteverantwortlicher':
            # Hinzugefügt: Übergeben der verantwortlichen Person und End of Life Datum an die add_device-Methode
            device_db = DeviceDatabase()  # Instanziere die DeviceDatabase-Klasse
            result = device_db.add_device(device_id, device_name, device_type, device_description, responsible_person, end_of_life)
            st.success(result)
        else:
            st.error("Nutzer ist nicht als Geräteverantwortlicher registriert.")

def modify_device():
    st.title("Gerät ändern")
    devices_db = DeviceDatabase()  # Instanziere die DeviceDatabase-Klasse
    devices = devices_db.get_all_devices()
    selected_device = st.selectbox("Gerät auswählen", devices)

    device_name = st.text_input("Neuer Gerätename", value=selected_device['device_name'])
    device_type = st.selectbox("Neuer Gerätetyp", ["Typ A", "Typ B", "Typ C"], index=["Typ A", "Typ B", "Typ C"].index(selected_device['device_type']))
    device_description = st.text_area("Neue Beschreibung", value=selected_device['device_description'])

    submitted = st.button("Änderungen speichern")
    
    if submitted:
        result = devices_db.modify_device(selected_device['device_id'], device_name, device_type, device_description)
        st.success(result)


def create_or_remove_reservation():
    st.title("Reservierung anlegen oder entfernen")
    devices_db = DeviceDatabase()
    users_db = UserDatabase()
    reservations_db = ReservationDatabase()

    devices = devices_db.get_all_devices()
    users = users_db.get_all_users()

    selected_device = st.selectbox("Gerät auswählen", devices)
    selected_user = st.selectbox("Nutzer auswählen", users)

    start_date = st.date_input("Startdatum")  # Keine zusätzliche Konvertierung notwendig
    end_date = st.date_input("Enddatum")  # Keine zusätzliche Konvertierung notwendig

    add_reservation = st.button("Reservierung anlegen")
    remove_reservation = st.button("Reservierung entfernen")

    if add_reservation:
        result = reservations_db.add_reservation(selected_device['device_id'], selected_user['user_id'], start_date, end_date)
        st.success(result)
    elif remove_reservation:
        result = reservations_db.remove_reservation(selected_device['device_id'], selected_user['user_id'], start_date, end_date)
        st.success(result)


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
