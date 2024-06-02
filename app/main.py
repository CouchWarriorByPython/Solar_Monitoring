from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from . import models, data_generator, schemas
from .database import engine, SessionLocal
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connections = []

current_indices = {
    "photo_sensors": 0,
    "temperature_sensors": 0,
    "voltage_sensors": 0,
    "current_sensors": 0
}


def initialize_data():
    with SessionLocal() as db:
        data_generator.initialize_test_solar_plants(db)


@app.on_event("startup")
async def startup_event():
    initialize_data()
    asyncio.create_task(schedule_data_generation())


async def schedule_data_generation():
    while True:
        with SessionLocal() as db:
            data_generator.generate_test_data(db)
            await notify_clients()
        await asyncio.sleep(60)


def convert_to_dict(sensor, location):
    """Converts Pydantic model to dict and formats datetime as string."""
    sensor_dict = sensor.dict()
    sensor_dict['location'] = location
    for key, value in sensor_dict.items():
        if isinstance(value, datetime):
            sensor_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    return sensor_dict


def get_recent_sensor_data(db, model, schema):
    sensors = db.query(model).order_by(model.timestamp.desc()).limit(10).all()
    return [convert_to_dict(schema.from_orm(sensor), sensor.plant.location) for sensor in sensors]


async def notify_clients():
    with SessionLocal() as db:
        data = {
            "photo_sensors": get_recent_sensor_data(db, models.PhotoSensor, schemas.PhotoSensor),
            "temperature_sensors": get_recent_sensor_data(db, models.TemperatureSensor, schemas.TemperatureSensor),
            "voltage_sensors": get_recent_sensor_data(db, models.VoltageSensor, schemas.VoltageSensor),
            "current_sensors": get_recent_sensor_data(db, models.CurrentSensor, schemas.CurrentSensor)
        }
        for connection in connections:
            await connection.send_json(data)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        with SessionLocal() as db:
            data = {
                "photo_sensors": get_recent_sensor_data(db, models.PhotoSensor, schemas.PhotoSensor),
                "temperature_sensors": get_recent_sensor_data(db, models.TemperatureSensor, schemas.TemperatureSensor),
                "voltage_sensors": get_recent_sensor_data(db, models.VoltageSensor, schemas.VoltageSensor),
                "current_sensors": get_recent_sensor_data(db, models.CurrentSensor, schemas.CurrentSensor)
            }
            await websocket.send_json(data)
        while True:
            await websocket.receive_text()
    except:
        connections.remove(websocket)


app.mount("/", StaticFiles(directory="static", html=True), name="static")

