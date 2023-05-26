from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from src import service
from src.schema import CreateGoodsSchema, AllGoodsSchema, OneGoodsSchema


router = APIRouter()


@router.post(path="/create_goods", status_code=201)
async def create_goods(goods: CreateGoodsSchema, db: Session = Depends(get_db)):
    await service.create_goods(goods=goods, db=db)


@router.delete(path="/delete_goods", status_code=204)
async def delete_goods(goods_id: int, db: Session = Depends(get_db)):
    await service.delete_goods(goods_id=goods_id, db=db)


@router.get(path="/get_goods", response_model=OneGoodsSchema, status_code=200)
async def get_goods(goods_id: int, db: Session = Depends(get_db)):
    return await service.get_goods(goods_id=goods_id, db=db)


@router.get(path="/get_all_goods", response_model=list[AllGoodsSchema], status_code=200)
async def get_all_goods(db: Session = Depends(get_db)):
    return await service.get_all_goods(db=db)


@router.patch(path="/update_goods", status_code=204)
async def update_goods(goods_id: int, weight: int, description: str, db: Session = Depends(get_db)):
    await service.update_goods(goods_id=goods_id, weight=weight, description=description, db=db)


@router.patch(path="/update_car", status_code=204)
async def update_car(car_id: int, zipcode: int, db: Session = Depends(get_db)):
    await service.update_car(car_id=car_id, zipcode=zipcode, db=db)


