from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
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

# Инициализация индексов для каждого типа сенсора
current_indices = {
    "photo_sensors": 0,
    "temperature_sensors": 0,
    "voltage_sensors": 0,
    "current_sensors": 0
}


def initialize_data():
    db: Session = SessionLocal()
    try:
        data_generator.initialize_test_solar_plants(db)
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    initialize_data()
    asyncio.create_task(schedule_data_generation())


async def schedule_data_generation():
    while True:
        db: Session = SessionLocal()
        try:
            data_generator.generate_test_data(db)
            await notify_clients()
            await asyncio.sleep(60)  # Ждем одну минуту
        finally:
            db.close()


def convert_to_dict(sensor, location):
    """Converts Pydantic model to dict and formats datetime as string."""
    sensor_dict = sensor.dict()
    sensor_dict['location'] = location
    for key, value in sensor_dict.items():
        if isinstance(value, datetime):
            sensor_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    return sensor_dict


async def notify_clients():
    db: Session = SessionLocal()
    try:
        photo_sensors = db.query(models.PhotoSensor).order_by(models.PhotoSensor.timestamp.desc()).limit(10).all()
        temperature_sensors = db.query(models.TemperatureSensor).order_by(models.TemperatureSensor.timestamp.desc()).limit(10).all()
        voltage_sensors = db.query(models.VoltageSensor).order_by(models.VoltageSensor.timestamp.desc()).limit(10).all()
        current_sensors = db.query(models.CurrentSensor).order_by(models.CurrentSensor.timestamp.desc()).limit(10).all()

        data = {
            "photo_sensors": [convert_to_dict(schemas.PhotoSensor.from_orm(sensor), sensor.plant.location) for sensor in photo_sensors],
            "temperature_sensors": [convert_to_dict(schemas.TemperatureSensor.from_orm(sensor), sensor.plant.location) for sensor in temperature_sensors],
            "voltage_sensors": [convert_to_dict(schemas.VoltageSensor.from_orm(sensor), sensor.plant.location) for sensor in voltage_sensors],
            "current_sensors": [convert_to_dict(schemas.CurrentSensor.from_orm(sensor), sensor.plant.location) for sensor in current_sensors]
        }

        for connection in connections:
            await connection.send_json(data)
    finally:
        db.close()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        db: Session = SessionLocal()
        try:
            photo_sensors = db.query(models.PhotoSensor).order_by(models.PhotoSensor.timestamp.desc()).limit(10).all()
            temperature_sensors = db.query(models.TemperatureSensor).order_by(models.TemperatureSensor.timestamp.desc()).limit(10).all()
            voltage_sensors = db.query(models.VoltageSensor).order_by(models.VoltageSensor.timestamp.desc()).limit(10).all()
            current_sensors = db.query(models.CurrentSensor).order_by(models.CurrentSensor.timestamp.desc()).limit(10).all()

            data = {
                "photo_sensors": [convert_to_dict(schemas.PhotoSensor.from_orm(sensor), sensor.plant.location) for sensor in photo_sensors],
                "temperature_sensors": [convert_to_dict(schemas.TemperatureSensor.from_orm(sensor), sensor.plant.location) for sensor in temperature_sensors],
                "voltage_sensors": [convert_to_dict(schemas.VoltageSensor.from_orm(sensor), sensor.plant.location) for sensor in voltage_sensors],
                "current_sensors": [convert_to_dict(schemas.CurrentSensor.from_orm(sensor), sensor.plant.location) for sensor in current_sensors]
            }
            await websocket.send_json(data)
        finally:
            db.close()

        while True:
            await websocket.receive_text()  # ожидание сообщений от клиента
    except:
        connections.remove(websocket)


# Подключение статических файлов
app.mount("/", StaticFiles(directory="static", html=True), name="static")