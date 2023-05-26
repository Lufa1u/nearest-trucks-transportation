from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_db
from src import service
from src.schema import CreateGoodsSchema, AllGoodsSchema, OneGoodsSchema

router = APIRouter()


@router.post(path="/create_goods", status_code=201)
async def create_goods(goods: CreateGoodsSchema, db: Session = Depends(get_db)):
    await service.create_goods(goods=goods, db=db)


@router.get(path="/get_goods", response_model=OneGoodsSchema)
async def get_goods(goods_id: int, db: Session = Depends(get_db)):
    return await service.get_goods(goods_id=goods_id, db=db)


@router.get(path="/get_all_goods", response_model=list[AllGoodsSchema])
async def get_all_goods(db: Session = Depends(get_db)):
    return await service.get_all_goods(db=db)

