from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey


Base = declarative_base()


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, index=True, unique=True)

    weight = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    pickup_location_id = Column(Integer, ForeignKey('location.id'))
    delivery_location_id = Column(Integer, ForeignKey('location.id'))

    pickup_location = relationship("Location", back_populates="pickup_goods", foreign_keys="Goods.pickup_location_id")
    delivery_location = relationship("Location", back_populates="delivery_goods", foreign_keys="Goods.delivery_location_id")


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, index=True, unique=True)

    city = Column(String, nullable=False)
    zip = Column(Integer, nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    cars = relationship("Car", back_populates="location")

    pickup_goods = relationship("Goods", foreign_keys="Goods.pickup_location_id", back_populates="pickup_location")
    delivery_goods = relationship("Goods", foreign_keys="Goods.delivery_location_id", back_populates="delivery_location")


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True, index=True, unique=True)

    number = Column(String, nullable=False, unique=True)
    load_capacity = Column(Integer, nullable=False)

    location_id = Column(Integer, ForeignKey('location.id'))

    location = relationship("Location", back_populates="cars")
