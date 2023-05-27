from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from src.model import Location, Goods, Car
from src.schema import CreateGoodsSchema


async def create_goods(goods: CreateGoodsSchema, db: Session):
    if goods.weight > 1000:
        raise HTTPException(status_code=422, detail="Weight can't be more than 1000.")
    if goods.pickup_zipcode == goods.delivery_zipcode:
        raise HTTPException(status_code=400, detail="Посылка для будущего тебя?)")
    locations = db.query(Location).filter(or_((Location.zip == goods.pickup_zipcode),
                                              (Location.zip == goods.delivery_zipcode))).all()
    if len(locations) < 2:
        raise HTTPException(status_code=404, detail="Location not found.")

    new_goods = Goods(weight=goods.weight, description=goods.description,
                      pickup_location_id=locations[0].id, delivery_location_id=locations[1].id)
    db.add(new_goods)
    db.commit()


async def delete_goods(goods_id: int, db: Session):
    goods = db.query(Goods).filter(Goods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found.")
    db.delete(goods)
    db.commit()


async def get_goods_location(pickup_location_id: int, db: Session):
    return db.query(Location.latitude, Location.longitude).filter(Location.id == pickup_location_id).first()


async def get_goods(goods_id: int, db: Session):
    goods = db.query(Goods).add_columns(Location.latitude, Location.longitude).where(
        Location.id == Goods.pickup_location_id or Location.id == Goods.delivery_location_id).filter(Goods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found.")
    return goods


async def get_all_goods(db: Session):
    return db.query(Goods).add_columns(Location.latitude, Location.longitude).where(
        Location.id == Goods.pickup_location_id or Location.id == Goods.delivery_location_id).all()


async def get_all_cars(db: Session):
    return db.query(Car.number).join(Location).add_columns(Location.latitude, Location.longitude).all()


async def update_goods(goods_id: int, weight: int, description: str, db: Session):
    if weight > 1000:
        raise HTTPException(status_code=422, detail="Weight can't be more than 1000.")
    goods = db.query(Goods).filter(Goods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found.")
    goods.weight = weight
    goods.description = description
    db.commit()


async def update_car(car_id: int, zipcode: int, db: Session):
    car = db.query(Car).filter(Car.id == car_id).first()
    location = db.query(Location).filter(Location.zip == zipcode).first()
    if not car or not location:
        raise HTTPException(status_code=422, detail="Incorrect car_id or zipcode.")
    car.location_id = location.id
    db.commit()
