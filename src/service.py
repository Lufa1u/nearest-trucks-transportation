from sqlalchemy.orm import Session

from src import manager
from src.schema import CreateGoodsSchema, CarsSchema


async def create_goods(goods: CreateGoodsSchema, db: Session):
    await manager.create_goods(goods=goods, db=db)


async def delete_goods(goods_id: int, db: Session):
    await manager.delete_goods(goods_id=goods_id, db=db)


async def get_goods(goods_id: int, db: Session):
    cars = [CarsSchema(number="3453B", distance=10)] #TODO функция получения всех машин
    return await manager.get_goods(goods_id=goods_id, cars=cars, db=db)


async def get_all_goods(db: Session):
    cars_amount = await get_cars_amount(db=db)
    return await manager.get_all_goods(cars_amount=cars_amount, db=db)


async def update_goods(goods_id: int, weight: int, description: str, db: Session):
    await manager.update_goods(goods_id=goods_id, weight=weight, description=description, db=db)


async def update_car(car_id: int, zipcode: int, db: Session):
    await manager.update_car(car_id=car_id, zipcode=zipcode, db=db)


async def get_cars_amount(db: Session):
    return 0 # TODO получение числа машин (расстояние <= 450)

