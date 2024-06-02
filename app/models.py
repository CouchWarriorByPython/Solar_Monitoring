from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class SolarPlant(Base):
    __tablename__ = 'solar_plants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    photo_sensors = relationship("PhotoSensor", back_populates="plant")
    temperature_sensors = relationship("TemperatureSensor", back_populates="plant")
    voltage_sensors = relationship("VoltageSensor", back_populates="plant")
    current_sensors = relationship("CurrentSensor", back_populates="plant")


class PhotoSensor(Base):
    __tablename__ = 'photo_sensors'

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey('solar_plants.id'))
    reading = Column(Float)
    timestamp = Column(DateTime)
    plant = relationship("SolarPlant", back_populates="photo_sensors")


class TemperatureSensor(Base):
    __tablename__ = 'temperature_sensors'

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey('solar_plants.id'))
    reading = Column(Float)
    timestamp = Column(DateTime)
    plant = relationship("SolarPlant", back_populates="temperature_sensors")


class VoltageSensor(Base):
    __tablename__ = 'voltage_sensors'

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey('solar_plants.id'))
    reading = Column(Float)
    timestamp = Column(DateTime)
    plant = relationship("SolarPlant", back_populates="voltage_sensors")


class CurrentSensor(Base):
    __tablename__ = 'current_sensors'

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey('solar_plants.id'))
    reading = Column(Float)
    timestamp = Column(DateTime)
    plant = relationship("SolarPlant", back_populates="current_sensors")
