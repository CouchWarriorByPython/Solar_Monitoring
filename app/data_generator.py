import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app import models


def generate_random_reading(min_val, max_val, decimal_places=0):
    return round(random.uniform(min_val, max_val), decimal_places)


def generate_test_data(db: Session):
    plants = db.query(models.SolarPlant).all()
    current_time = datetime.now(timezone.utc)

    for plant in plants:
        db.add(models.PhotoSensor(
            plant_id=plant.id,
            reading=generate_random_reading(0, 100000),
            timestamp=current_time
        ))
        db.add(models.TemperatureSensor(
            plant_id=plant.id,
            reading=generate_random_reading(-40, 80, 2),
            timestamp=current_time
        ))
        db.add(models.VoltageSensor(
            plant_id=plant.id,
            reading=generate_random_reading(0, 25, 2),
            timestamp=current_time
        ))
        db.add(models.CurrentSensor(
            plant_id=plant.id,
            reading=generate_random_reading(0, 10, 2),
            timestamp=current_time
        ))

    db.commit()


def initialize_test_solar_plants(db: Session):
    locations = [
        "Location A", "Location B", "Location C", "Location D", "Location E", "Location F", "Location G",
        "Location H", "Location I", "Location J"
    ]
    plants_count = db.query(models.SolarPlant).count()

    if plants_count == 0:
        for location in locations:
            test_plant = models.SolarPlant(name=f"Test Plant {location}", location=location)
            db.add(test_plant)
        db.commit()
