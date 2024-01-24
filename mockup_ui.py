import streamlit as st
from backend import UserDatabase, DeviceDatabase  # Updated import statements

def create_new_user(user_db):
    st.title("Nutzer anlegen")
    username = st.text_input("Benutzername")
    email = st.text_input("E-Mail")
    role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])
    
    submitted = st.button("Nutzer anlegen")
    
    if submitted:
        result = user_db.add_user(username, email, role)
        st.success(result)

def create_or_modify_device(device_db, user_db):
    st.title("Gerät anlegen")
    device_id = st.number_input("ID/ Inventarnummer", step=1, value=0)
    device_name = st.text_input("Gerätename")
    device_type = st.selectbox("Gerätetyp", ["Typ A", "Typ B", "Typ C"])
    device_description = st.text_area("Beschreibung")

    # Hinzugefügt: Informationen über den verantwortlichen Benutzer
    responsible_person_name = st.text_input("Name des verantwortlichen Benutzers")
    responsible_person_email = st.text_input("E-Mail des verantwortlichen Benutzers")

    submitted = st.button("Gerät speichern")
    
    if submitted:
        # Überprüfen Sie, ob device_id leer ist, und verwenden Sie 0 als Dummy-Wert
        device_id = int(device_id) if device_id else 0

        # Überprüfen Sie, ob der verantwortliche Benutzer als Geräteverantwortlicher registriert ist
        responsible_person = user_db.get_user_by_name_and_email(responsible_person_name, responsible_person_email)
        if responsible_person and responsible_person['role'] == 'Geräteverantwortlicher':
            # Hinzugefügt: Übergeben der verantwortlichen Person an die add_device-Methode
            result = device_db.add_device(device_id, device_name, device_type, device_description, responsible_person)
            st.success(result)
        else:
            st.error("Nutzer ist nicht als Geräteverantwortlicher registriert.")



def modify_device(device_db, user_db):
    st.title("Gerät ändern")
    devices = device_db.get_all_devices()
    selected_device = st.selectbox("Gerät auswählen", devices)

    # Informationen zum ausgewählten Gerät anzeigen
    st.write("Ausgewähltes Gerät:")
    st.write(f"- ID/Inventarnummer: {selected_device['device_id']}")
    st.write(f"- Gerätename: {selected_device['device_name']}")
    st.write(f"- Gerätetyp: {selected_device['device_type']}")
    st.write(f"- Beschreibung: {selected_device['device_description']}")
    st.write(f"- Verantwortliche Person: {selected_device['responsible_person']['username']}")

    # Eingabefelder für die Aktualisierung der Geräteinformationen
    device_name = st.text_input("Neuer Gerätename", selected_device['device_name'])
    device_type = st.selectbox("Neuer Gerätetyp", ["Typ A", "Typ B", "Typ C"], index=["Typ A", "Typ B", "Typ C"].index(selected_device['device_type']))
    device_description = st.text_area("Neue Beschreibung", selected_device['device_description'])

    submitted = st.button("Gerät aktualisieren")

    if submitted:
        # Aktualisierte Geräteinformationen speichern
        updated_device = {
            "device_id": selected_device['device_id'],
            "device_name": device_name,
            "device_type": device_type,
            "device_description": device_description,
            "responsible_person": selected_device['responsible_person']
        }
        result = device_db.modify_device(updated_device)
        st.success(result)
        


def manage_reservations(device_db):
    st.title("Reservierung anlegen/entfernen")
    devices = device_db.get_all_devices()
    selected_device = st.selectbox("Gerät auswählen", devices)

    existing_reservations_for_device = device_db.get_reservations_for_device(selected_device)

    if existing_reservations_for_device:
        st.write("Bestehende Reservierungen:")
        for reservation in existing_reservations_for_device:
            st.write(f"- {reservation['user']}: {reservation['date']}")

    reservation_date = st.date_input("Reservierungsdatum")
    user = st.text_input("Benutzer für die Reservierung")

    submitted = st.button("Reservierung speichern")

    if submitted:
        device_db.add_reservation(selected_device, reservation_date, user)
        st.success(f"Reservierung für '{selected_device}' am '{reservation_date}' {'entfernt' if existing_reservations_for_device else 'angelegt'} für '{user}'.")

def maintenance_management(device_db):
    st.title("Wartungs-Management")
    devices = device_db.get_all_devices()
    selected_device = st.selectbox("Gerät auswählen", devices)

    next_maintenance = device_db.get_next_maintenance(selected_device)
    st.write(f"Nächste Wartung für '{selected_device}': {next_maintenance}")

    maintenance_costs = device_db.get_maintenance_costs(selected_device)
    st.write(f"Wartungskosten pro Quartal für '{selected_device}': {maintenance_costs} €")


def modify_device(device_db):
    st.title("Gerät ändern")
    devices = device_db.get_all_devices()
    selected_device = st.selectbox("Gerät auswählen", devices)

    device_name = st.text_input("Neuer Gerätename", value=selected_device['device_name'])
    device_type = st.selectbox("Neuer Gerätetyp", ["Typ A", "Typ B", "Typ C"], index=["Typ A", "Typ B", "Typ C"].index(selected_device['device_type']))
    device_description = st.text_area("Neue Beschreibung", value=selected_device['device_description'])

    submitted = st.button("Änderungen speichern")
    
    if submitted:
        result = device_db.modify_device(selected_device['device_id'], device_name, device_type, device_description)
        st.success(result)

def main():
    st.title("Geräte-Verwaltung")
    user_db = UserDatabase('users.json')
    device_db = DeviceDatabase('devices.json')
    action = st.sidebar.selectbox("Aktion auswählen", ["Nutzer anlegen", "Geräte anlegen", "Geräte ändern", "Reservierungssystem", "Wartungs-Management"])

    if action == "Nutzer anlegen":
        create_new_user(user_db)
    elif action == "Geräte anlegen":
        create_or_modify_device(device_db, user_db)
    elif action == "Geräte ändern":
        modify_device(device_db)
    elif action == "Reservierungssystem":
        manage_reservations(device_db)
    elif action == "Wartungs-Management":
        maintenance_management(device_db)

if __name__ == "__main__":
    main()
