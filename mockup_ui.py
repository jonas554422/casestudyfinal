import streamlit as st
from database import DeviceDatabase  # Corrected import statement




def create_new_user(db):
    st.title("Nutzer anlegen")
    username = st.text_input("Benutzername")
    email = st.text_input("E-Mail")
    role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])
    
    submitted = st.button("Nutzer anlegen")
    
    if submitted:
        # Hier kannst du die Nutzerdaten in der Datenbank speichern
        result = db.add_user(username, email, role)
        st.success(result)


def create_or_modify_device(db):
    st.title("Gerät anlegen/ändern")
    device_name = st.text_input("Gerätename")
    device_type = st.selectbox("Gerätetyp", ["Typ A", "Typ B", "Typ C"])
    device_description = st.text_area("Beschreibung")
    
    submitted = st.button("Gerät speichern")
    
    if submitted:
        # Hier kannst du die Gerätedaten in der Datenbank speichern oder aktualisieren
        result = db.add_device(device_name, device_type, device_description)
        st.success(result)
        # Anpassung: Statt der vorherigen Zeile, kannst du die oben stehende Zeile verwenden, um die Rückmeldung von add_device anzuzeigen

def manage_reservations(db):
    st.title("Reservierung anlegen/entfernen")
    devices = db.get_all_devices()  # Hier kannst du die tatsächlichen Geräte aus der Datenbank laden
    selected_device = st.selectbox("Gerät auswählen", devices)

    # Hier kannst du die tatsächlichen Reservierungen aus der Datenbank laden
    existing_reservations_for_device = db.get_reservations_for_device(selected_device)

    if existing_reservations_for_device:
        st.write("Bestehende Reservierungen:")
        for reservation in existing_reservations_for_device:
            st.write(f"- {reservation['user']}: {reservation['date']}")

    reservation_date = st.date_input("Reservierungsdatum")
    user = st.text_input("Benutzer für die Reservierung")

    submitted = st.button("Reservierung speichern")

    if submitted:
        # Hier kannst du die Reservierungsdaten in der Datenbank speichern oder entfernen
        db.add_reservation(selected_device, reservation_date, user)
        st.success(f"Reservierung für '{selected_device}' am '{reservation_date}' {'entfernt' if existing_reservations_for_device else 'angelegt'} für '{user}'.")

def maintenance_management(db):
    st.title("Wartungs-Management")
    devices = db.get_all_devices()  # Hier kannst du die tatsächlichen Geräte aus der Datenbank laden
    selected_device = st.selectbox("Gerät auswählen", devices)

    # Hier kannst du die tatsächlichen Wartungstermine aus der Datenbank laden
    next_maintenance = db.get_next_maintenance(selected_device)

    st.write(f"Nächste Wartung für '{selected_device}': {next_maintenance}")

    # Hier kannst du die tatsächlichen Wartungskosten aus der Datenbank laden
    maintenance_costs = db.get_maintenance_costs(selected_device)

    st.write(f"Wartungskosten pro Quartal für '{selected_device}': {maintenance_costs} €")

def main():
    st.title("Geräte-Verwaltung")
    db = DeviceDatabase('users.json')
    action = st.sidebar.selectbox("Aktion auswählen", ["Nutzer anlegen", "Geräte anlegen/ändern", "Reservierungssystem", "Wartungs-Management"])

    if action == "Nutzer anlegen":
        create_new_user(db)
    elif action == "Geräte anlegen/ändern":
        create_or_modify_device(db)
    elif action == "Reservierungssystem":
        manage_reservations(db)
    elif action == "Wartungs-Management":
        maintenance_management(db)

if __name__ == "__main__":
    from database import DeviceDatabase
    db = DeviceDatabase('users.json', 'devices.json')
    main()


