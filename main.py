from fastapi import FastAPI
from config import get_db
from src.model import Location
from src.service import upload_locations


app = FastAPI()

if __name__ == "__main__":
    db = get_db()
    if not (db.query(Location).first()):
        upload_locations(db=db)
    db.close()

