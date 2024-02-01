import streamlit as st
from backend import UserDatabase, DeviceDatabase, ReservationDatabase, MaintenanceDatabase
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
    st.title("Gerät anlegen oder ändern")
    device_db = DeviceDatabase()
    user_db = UserDatabase()

    device_id = st.number_input("ID/ Inventarnummer", step=1, value=0)
    device_name = st.text_input("Gerätename")
    device_type = st.selectbox("Gerätetyp", ["Typ A", "Typ B", "Typ C"])
    device_description = st.text_area("Beschreibung")
    responsible_person_name = st.text_input("Name des verantwortlichen Benutzers")
    responsible_person_email = st.text_input("E-Mail des verantwortlichen Benutzers")
    end_of_life = st.date_input("End of Life Datum (optional)")
    first_maintenance = st.date_input("Erste Wartung am")
    next_maintenance = st.date_input("Nächste Wartung am")
    maintenance_interval = st.number_input("Wartungsintervall in Tagen", step=1, min_value=1)
    maintenance_cost = st.number_input("Kosten pro Wartung", min_value=0.0, format="%.2f")

    submitted = st.button("Gerät speichern")
    if submitted:
        responsible_person = user_db.get_user_by_name_and_email(responsible_person_name, responsible_person_email)
        if responsible_person:
            result = device_db.add_device(device_id, device_name, device_type, device_description, responsible_person, end_of_life, first_maintenance, next_maintenance, maintenance_interval, maintenance_cost)
            st.success(result)
        else:
            st.error("Verantwortliche Person nicht gefunden.")



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

    # Auswahlboxen für Geräte und Nutzer
    devices = devices_db.get_all_devices()
    users = users_db.get_all_users()

    device_options = {device['device_id']: device for device in devices}
    user_options = {user['user_id']: user for user in users}

    selected_device_id = st.selectbox("Gerät auswählen", list(device_options.keys()), format_func=lambda x: device_options[x]['device_name'])
    selected_user_id = st.selectbox("Nutzer auswählen", list(user_options.keys()), format_func=lambda x: user_options[x]['username'])

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
    if current_reservations:
        for res in current_reservations:
            st.write(f"Gerät: {res['device_name']}, Nutzer: {res['user_name']}, Zeitraum: {res['start_date']} bis {res['end_date']}")
    else:
        st.write("Keine aktuellen Reservierungen vorhanden.")


def manage_maintenance():
    st.title("Wartungs-Management")
    maintenance_db = MaintenanceDatabase()

    st.subheader("Nächste Wartungstermine")
    next_maintenance_dates = maintenance_db.get_next_maintenance_dates()
    for maintenance in next_maintenance_dates:
        st.write(f"Gerät: {maintenance['device_name']}, Nächsten 4 Wartungen: {', '.join(maintenance['next_maintenances'])}")


    st.subheader("Wartungskosten pro Quartal")
    quarterly_costs = maintenance_db.calculate_quarterly_maintenance_costs()
    for quarter, cost in quarterly_costs.items():
        st.write(f"{quarter}: {cost} €")




def main():
    st.title("Geräte-Verwaltung")

    # Dictionary mit Aktionen und den zugehörigen Funktionen
    actions = {
        "Nutzer anlegen": create_new_user,
        "Geräte anlegen": create_or_modify_device,
        "Geräte ändern": modify_device,
        "Reservierung anlegen/entfernen": create_or_remove_reservation,
        "Wartungs-Management": manage_maintenance
    }

    # Initialisieren des Session States
    if 'current_action' not in st.session_state:
        st.session_state['current_action'] = None

    # Erstellen der Buttons und Aktualisieren des Session States bei Klick
    for action, function in actions.items():
        if st.sidebar.button(action, key=f"btn_{action}"):
            st.session_state['current_action'] = action

    # Aufrufen der entsprechenden Funktion basierend auf dem Session State
    if st.session_state['current_action']:
        actions[st.session_state['current_action']]()

if __name__ == "__main__":
    main()

