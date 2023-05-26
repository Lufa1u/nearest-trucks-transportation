from pydantic import BaseModel


class LocationSchema(BaseModel):
    id: int
    city: str
    zip: int
    latitude: float
    longitude: float


class Cars(BaseModel):
    number: str
    distance: float


class OneGoodsSchema(BaseModel):
    id: int
    weight: int
    description: str
    pickup_location: LocationSchema
    delivery_location: LocationSchema
    cars: list[Cars]


class AllGoodsSchema(BaseModel):
    id: int
    weight: int
    cars_amount: int
    description: str
    pickup_location: LocationSchema
    delivery_location: LocationSchema


class CreateGoodsSchema(BaseModel):
    weight: int
    description: str
    pickup_zipcode: int
    delivery_zipcode: int
