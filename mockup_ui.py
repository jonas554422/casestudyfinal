import streamlit as st

def create_new_user():
    st.title("Nutzer anlegen")
    username = st.text_input("Benutzername")
    email = st.text_input("E-Mail")
    role = st.selectbox("Rolle", ["Geräteverantwortlicher", "Reservierer"])
    
    submitted = st.button("Nutzer anlegen")
    
    if submitted:
        # Hier könntest du die Nutzerdaten speichern (zum Beispiel in einer Datenbank)
        st.success(f"Nutzer '{username}' erfolgreich angelegt als {role} mit der E-Mail '{email}'.")

def create_or_modify_device():
    st.title("Gerät anlegen/ändern")
    device_name = st.text_input("Gerätename")
    device_type = st.selectbox("Gerätetyp", ["Typ A", "Typ B", "Typ C"])
    device_description = st.text_area("Beschreibung")
    
    submitted = st.button("Gerät speichern")
    
    if submitted:
        # Hier könntest du die Gerätedaten speichern oder aktualisieren
        st.success(f"Gerät '{device_name}' erfolgreich gespeichert als '{device_type}'.")

def manage_reservations():
    st.title("Reservierung anlegen/entfernen")
    devices = ["Gerät A", "Gerät B", "Gerät C"]  # Hier könntest du die tatsächlichen Geräte laden
    selected_device = st.selectbox("Gerät auswählen", devices)

    # Simulieren bereits bestehende Reservierungen für das gewählte Gerät
    existing_reservations = []  # Hier könntest du die tatsächlichen Reservierungen laden
    existing_reservations_for_device = [r for r in existing_reservations if r['device'] == selected_device]

    if existing_reservations_for_device:
        st.write("Bestehende Reservierungen:")
        for reservation in existing_reservations_for_device:
            st.write(f"- {reservation['user']}: {reservation['date']}")

    reservation_date = st.date_input("Reservierungsdatum")
    user = st.text_input("Benutzer für die Reservierung")

    submitted = st.button("Reservierung speichern")

    if submitted:
        # Hier könntest du die Reservierungsdaten speichern oder entfernen
        if existing_reservations_for_device:
            st.success(f"Reservierung für '{selected_device}' am '{reservation_date}' entfernt für '{user}'.")
        else:
            st.success(f"Reservierung für '{selected_device}' am '{reservation_date}' angelegt für '{user}'.")

def maintenance_management():
    st.title("Wartungs-Management")
    devices = ["Gerät A", "Gerät B", "Gerät C"]  # Hier könntest du die tatsächlichen Geräte laden
    selected_device = st.selectbox("Gerät auswählen", devices)

    # Simulieren nächste Wartungstermine für das gewählte Gerät
    next_maintenance = {}  # Hier könntest du die tatsächlichen Wartungstermine laden
    next_maintenance[selected_device] = "31. März 2024"  # Beispiel für den nächsten Wartungstermin

    st.write(f"Nächste Wartung für '{selected_device}': {next_maintenance[selected_device]}")

    # Simulieren Wartungskosten pro Quartal für das gewählte Gerät
    maintenance_costs = {}  # Hier könntest du die tatsächlichen Kosten laden
    maintenance_costs[selected_device] = 1500  # Beispiel für die Wartungskosten pro Quartal

    st.write(f"Wartungskosten pro Quartal für '{selected_device}': {maintenance_costs[selected_device]} €")

def main():
    st.title("Geräte-Verwaltung")
    action = st.sidebar.selectbox("Aktion auswählen", ["Nutzer anlegen", "Geräte anlegen/ändern", "Reservierungssystem", "Wartungs-Management"])

    if action == "Nutzer anlegen":
        create_new_user()
    elif action == "Geräte anlegen/ändern":
        create_or_modify_device()
    elif action == "Reservierungssystem":
        manage_reservations()
    elif action == "Wartungs-Management":
        maintenance_management()

if __name__ == "__main__":
    main()
