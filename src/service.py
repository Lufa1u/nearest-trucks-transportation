from sqlalchemy.orm import Session

from src import manager
from src.schema import CreateGoodsSchema, Cars


async def create_goods(goods: CreateGoodsSchema, db: Session):
    await manager.create_goods(goods=goods, db=db)


async def get_goods(goods_id: int, db: Session):
    cars = [Cars(number="3453B", distance=10)] #TODO функция получения всех машин
    return await manager.get_goods(goods_id=goods_id, cars=cars, db=db)


async def get_all_goods(db: Session):
    cars_amount = await get_cars_amount(db=db)
    return await manager.get_all_goods(cars_amount=cars_amount, db=db)


async def get_cars_amount(db: Session):
    return 0 # TODO получение числа машин (расстояние <= 450)

