import csv

from sqlalchemy.orm import Session

from src.model import Location
from src import manager


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
    manager.upload_locations(locations=locations, db=db)
