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
    all_cars = await manager.get_all_cars(db=db)
    goods, goods_lan, goods_lon = await manager.get_goods(goods_id=goods_id, db=db)

    for number, car_lan, car_lon in all_cars:
        distance = await calculate_distance((car_lan, car_lon), (goods_lan, goods_lon))
        cars.append({"number": number, "distance": distance})

    return OneGoodsSchema(id=goods.id, weight=goods.weight, cars=cars,
                          description=goods.description, pickup_location=goods.pickup_location.__dict__,
                          delivery_location=goods.delivery_location.__dict__)


async def get_all_goods(db: Session):
    result = []
    all_cars = await manager.get_all_cars(db=db)
    all_goods = await manager.get_all_goods(db=db)
    for goods, goods_lan, goods_lon in all_goods:
        distances = []
        for number, car_lan, car_lon in all_cars:
            distance = await calculate_distance((car_lan, car_lon), (goods_lan, goods_lon))
            if distance <= 450:
                distances.append(distance)

        result.append(AllGoodsSchema(id=goods.id, weight=goods.weight,
                                     description=goods.description, cars_amount=len(distances),
                                     pickup_location=goods.pickup_location.__dict__, delivery_location=goods.delivery_location.__dict__))
    return result


async def get_goods_with_filters(db: Session, weight_limit: int = None, distance_limit: int = 1000):
    result = []
    all_cars = await manager.get_all_cars(db=db)
    all_goods = await manager.get_all_goods(db=db, weight_limit=weight_limit)
    for goods, goods_lan, goods_lon in all_goods:
        distances = []
        for number, car_lan, car_lon in all_cars:
            distance = await calculate_distance((car_lan, car_lon), (goods_lan, goods_lon))
            if (distance_limit and distance <= distance_limit) or (not distance_limit):
                distances.append(distance)

        if distances:
            result.append(AllGoodsSchema(id=goods.id, weight=goods.weight,
                                         description=goods.description, cars_amount=len(distances),
                                         pickup_location=goods.pickup_location.__dict__,
                                         delivery_location=goods.delivery_location.__dict__))
    return result


async def update_goods(goods_id: int, weight: int, description: str, db: Session):
    await manager.update_goods(goods_id=goods_id, weight=weight, description=description, db=db)


async def update_car(car_id: int, zipcode: int, db: Session):
    await manager.update_car(car_id=car_id, zipcode=zipcode, db=db)


async def calculate_distance(location_from: tuple, location_to: tuple):
    return gd(location_from, location_to).mi


