from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Boolean
from sqlalchemy.orm import relationship
from database import Base, engine


class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True)
    year_of_manufacture = Column(Integer)
    number = Column(Integer)
    brand = Column(String)
    full_name = Column(String)
    orders = relationship("Order", back_populates="car")


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    date_of_issue = Column(Date)
    price = Column(Integer)
    real_end_date = Column(Date)
    planning_date_of_end = Column(Date)
    type_of_work = Column(String)
    car_id = Column(Integer, ForeignKey('car.id'))
    car = relationship("Car", back_populates="orders")

    mechanic_id = Column(Integer, ForeignKey('mechanic.id'))
    mechanic = relationship("Mechanic", back_populates="orders")


class Mechanic(Base):
    __tablename__ = "mechanic"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    table_number = Column(Integer)
    experience = Column(Integer)
    rank = Column(String)        
    orders = relationship("Order", back_populates="mechanic")


Base.metadata.create_all(engine)