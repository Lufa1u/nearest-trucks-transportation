import csv
import random
import string

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from config import get_db
from src.model import Location, Car


def upload_random_cars(db: Session):
    min_id, max_id = list(db.query(func.min(Location.id), func.max(Location.id)).first())
    cars = []
    for i in range(20):
        car = Car(
            number=f"{str(random.randint(1000, 9999))}{random.choice(string.ascii_uppercase)}",
            load_capacity=random.randint(1, 1000),
            location_id=random.randint(min_id, max_id)
        )
        cars.append(car)
    db.add_all(cars)
    db.commit()


def upload_locations(db: Session):
    locations = []
    with open('uszips.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            items = ''.join(row).replace('"', '').split(",")
            if items[0] == "zip":
                continue
            location = Location(zip=items[0], latitude=items[1], longitude=items[2], city=items[3])
            locations.append(location)
    db.add_all(locations)
    db.commit()


if __name__ == "__main__":
    db = get_db()
    if not (db.query(Location).first()):
        upload_locations(db=db)
        upload_random_cars(db=db)
    db.close()
