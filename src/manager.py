from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from src.model import Location, Goods
from src.schema import CreateGoodsSchema, AllGoodsSchema, OneGoodsSchema, Cars


async def create_goods(goods: CreateGoodsSchema, db: Session):
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


async def get_goods(goods_id: int, cars: list[Cars], db: Session):
    goods = db.query(Goods).filter(Goods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found.")
    return OneGoodsSchema(id=goods.id, weight=goods.weight, cars=cars,
                          description=goods.description, pickup_location=goods.pickup_location.__dict__,
                          delivery_location=goods.delivery_location.__dict__)


async def get_all_goods(cars_amount: int, db: Session):
    result = []
    items = db.query(Goods).where(or_((Location.id == Goods.pickup_location_id),
                                      (Location.id == Goods.delivery_location_id))).all()
    for item in items:
        goods = AllGoodsSchema(id=item.id, weight=item.weight, cars_amount=cars_amount,
                               description=item.description, pickup_location=item.pickup_location.__dict__,
                               delivery_location=item.delivery_location.__dict__)
        result.append(goods)
    return result
