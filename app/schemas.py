from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PhotoSensorBase(BaseModel):
    reading: float
    timestamp: datetime


class PhotoSensorCreate(PhotoSensorBase):
    pass


class PhotoSensor(PhotoSensorBase):
    id: int
    plant_id: int

    class Config:
        from_attributes = True


class TemperatureSensorBase(BaseModel):
    reading: float
    timestamp: datetime


class TemperatureSensorCreate(TemperatureSensorBase):
    pass


class TemperatureSensor(TemperatureSensorBase):
    id: int
    plant_id: int

    class Config:
        from_attributes = True


class VoltageSensorBase(BaseModel):
    reading: float
    timestamp: datetime


class VoltageSensorCreate(VoltageSensorBase):
    pass


class VoltageSensor(VoltageSensorBase):
    id: int
    plant_id: int

    class Config:
        from_attributes = True


class CurrentSensorBase(BaseModel):
    reading: float
    timestamp: datetime


class CurrentSensorCreate(CurrentSensorBase):
    pass


class CurrentSensor(CurrentSensorBase):
    id: int
    plant_id: int

    class Config:
        from_attributes = True


class SolarPlantBase(BaseModel):
    name: str
    location: str


class SolarPlantCreate(SolarPlantBase):
    pass


class SolarPlant(SolarPlantBase):
    id: int
    photo_sensors: List[PhotoSensor] = []
    temperature_sensors: List[TemperatureSensor] = []
    voltage_sensors: List[VoltageSensor] = []
    current_sensors: List[CurrentSensor] = []

    class Config:
        from_attributes = True
