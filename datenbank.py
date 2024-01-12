from fastapi import FastAPI, HTTPException
from tinydb import TinyDB, Query
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Verbindung zur TinyDB-Datenbank herstellen
db = TinyDB('database.json')
devices_table = db.table('devices')
users_table = db.table('users')
reservations_table = db.table('reservations')

class Device(BaseModel):
    device_name: str
    device_type: str
    device_description: str

class User(BaseModel):
    username: str
    email: str
    role: str

class Reservation(BaseModel):
    device_name: str
    reservation_date: str
    user: str

# Funktionen für die Datenbank-Operationen
def find_devices() -> List[str]:
    devices = devices_table.all()
    return [device['device_name'] for device in devices]

def create_device(device: Device):
    devices_table.insert(device.dict())

def find_users() -> List[str]:
    users = users_table.all()
    return [user['username'] for user in users]

def create_user(user: User):
    users_table.insert(user.dict())

def find_reservations() -> List[Reservation]:
    reservations = reservations_table.all()
    return [Reservation(**reservation) for reservation in reservations]

def create_reservation(reservation: Reservation):
    reservations_table.insert(reservation.dict())

# API-Endpunkte
@app.get("/devices", response_model=List[str])
def read_devices():
    return find_devices()

@app.post("/devices", status_code=201)
def create_new_device(device: Device):
    create_device(device)
    return {"message": "Device created successfully"}

@app.get("/users", response_model=List[str])
def read_users():
    return find_users()

@app.post("/users", status_code=201)
def create_new_user(user: User):
    create_user(user)
    return {"message": "User created successfully"}

@app.get("/reservations", response_model=List[Reservation])
def read_reservations():
    return find_reservations()

@app.post("/reservations", status_code=201)
def create_new_reservation(reservation: Reservation):
    create_reservation(reservation)
    return {"message": "Reservation created successfully"}
