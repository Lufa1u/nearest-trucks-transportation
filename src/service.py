from sqlalchemy.orm import Session

from src import manager
from src.schema import CreateGoodsSchema, OneGoodsSchema, AllGoodsSchema
from geopy.distance import geodesic as gd


async def create_goods(goods: CreateGoodsSchema, db: Session):
    await manager.create_goods(goods=goods, db=db)


async def delete_goods(goods_id: int, db: Session):
    await manager.delete_goods(goods_id=goods_id, db=db)


async def get_goods(goods_id: int, db: Session):
    cars = []
    all_cars = await get_all_cars(db=db)
    goods, lan, lon = await manager.get_goods(goods_id=goods_id, db=db)

    for car in all_cars:
        distance = await calculate_distance((car[1], car[2]), (lan, lon))
        cars.append({"number": car.number, "distance": distance})

    return OneGoodsSchema(id=goods.id, weight=goods.weight, cars=cars,
                          description=goods.description, pickup_location=goods.pickup_location.__dict__,
                          delivery_location=goods.delivery_location.__dict__)


async def get_all_goods(db: Session):
    result = []
    distances = []
    all_cars = await get_all_cars(db=db)
    all_goods = await manager.get_all_goods(db=db)
    for goods, lan, lon in all_goods:
        for car in all_cars:
            distances.append(await calculate_distance((car[1], car[2]), (lan, lon)))

        result.append(AllGoodsSchema(id=goods.id, weight=goods.weight,
                                     description=goods.description, cars_amount=len([item for item in distances if item <= 450]),
                                     pickup_location=goods.pickup_location.__dict__, delivery_location=goods.delivery_location.__dict__))
        distances = []
    return result


async def update_goods(goods_id: int, weight: int, description: str, db: Session):
    await manager.update_goods(goods_id=goods_id, weight=weight, description=description, db=db)


async def update_car(car_id: int, zipcode: int, db: Session):
    await manager.update_car(car_id=car_id, zipcode=zipcode, db=db)


async def get_all_cars(db: Session):
    return await manager.get_all_cars(db=db)


async def calculate_distance(location_from: tuple, location_to: tuple):
    return gd(location_from, location_to).mi


