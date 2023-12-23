from datetime import date
from pydantic import BaseModel
from models import Car, Mechanic, Order
from database import Base, engine, SessionLocal
from fastapi import FastAPI, HTTPException, Depends,Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import update


app = FastAPI()
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Car_delete(BaseModel):
    message:str


class Order_delete(BaseModel):
    message:str


class Mechanic_delete(BaseModel):
    message:str


class Car_create(BaseModel):
    year_of_manufacture: int
    number: int
    brand: str
    full_name: str


class Car_response(BaseModel):
    year_of_manufacture: int
    number: int
    brand: str
    full_name: str
    id: int

    
class Order_create(BaseModel):
    date_of_issue: date
    price: int
    real_end_date: date
    planning_date_of_end: date
    type_of_work: str


class Order_response(BaseModel):
    id: int
    date_of_issue: date
    price: int
    real_end_date: date
    planning_date_of_end: date
    type_of_work: str 


class mechanic_create(BaseModel):
    full_name: str
    table_number: int
    experience: int
    rank: str                       


class mechanic_response(BaseModel):
    id: int
    full_name: str
    table_number: int
    experience: int
    rank: str


@app.post("/car/", response_model=Car_response)
def post_car(car: Car_create, db: Session=Depends(get_db)): 
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car    


@app.post("/order/", response_model=Order_response)
def post_order(order: Order_create, db: Session=Depends(get_db)): 
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.post("/mechanic/", response_model=mechanic_response)
def post_mechanic(mechanic: mechanic_create, db: Session=Depends(get_db)): 
    db_mechanic = Mechanic(**mechanic.dict())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic


@app.get("/car/{car_id}", response_model=Car_response)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return car


@app.get("/order/{order_id}", response_model=Order_response)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order not found')
    return order


@app.get("/mechanic/{mechanic_id}", response_model=mechanic_response)
def read_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(Mechanic).filter(Mechanic.id == mechanic_id).first()
    if mechanic is None:
        raise HTTPException(status_code=404, detail='Mechanic not found')
    return mechanic


@app.put("/car/{car_id}", response_model=Car_response)
def update_car(car_id: int, updated: Car_create, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail='Car type not found')

    for key, value in updated.dict().items():
        setattr(car, key, value)

    db.commit()
    db.refresh(car)
    return car


@app.put("/order/{order_id}", response_model=Order_response)
def update_order(order_id: int, updated: Order_create, db: Session = Depends(get_db)):
    order = db.query(order).filter(order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order type not found')

    for key, value in updated.dict().items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@app.put("/mechanic/{mechanic_id}", response_model=mechanic_response)
def update_mechanic(mechanic_id: int, updated: mechanic_create, db: Session = Depends(get_db)):
    mechanic = db.query(mechanic).filter(mechanic.id == mechanic_id).first()
    if mechanic is None:
        raise HTTPException(status_code=404, detail='Mechanic type not found')

    for key, value in updated.dict().items():
        setattr(mechanic, key, value)

    db.commit()
    db.refresh(mechanic)
    return mechanic


@app.delete("/car/{car_id}", response_model=Car_delete)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(car).filter(car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()
    return {"message": "car deleted"}


@app.delete("/order/{order_id}", response_model=Order_delete)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(order).filter(order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "order deleted"}


@app.delete("/mechanic/{mechanic_id}", response_model=Mechanic_delete)
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(mechanic).filter(mechanic.id == mechanic_id).first()
    if mechanic is None:
        raise HTTPException(status_code=404, detail="mechanic not found")

    db.delete(mechanic)
    db.commit()
    return {"message": "mechanic deleted"}


@app.get("/car/", response_model=List[Car_response])
def read_cars(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    car = db.query(Car).offset(page).limit(per_page).all()
    if car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return car


@app.get("/order/", response_model=List[Order_response])
def read_orders(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    order = db.query(order).offset(page).limit(per_page).all()
    if order is None:
        raise HTTPException(status_code=404, detail='order not found')
    return order


@app.get("/mechanic/", response_model=List[mechanic_response])
def read_mechanics(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    mechanic = db.query(mechanic).offset(page).limit(per_page).all()
    if mechanic is None:
        raise HTTPException(status_code=404, detail='mechanic not found')
    return mechanic


@app.get("/cars_by_condition/", response_model=List[Car_response])
def get_cars_by_condition(
    year_of_manufacture: int = Query(None, description="Filter by year of manufacture"),
    brand: str = Query(None, description="Filter by brand"),
    db: Session = Depends(get_db)
):
    conditions = []
    if year_of_manufacture:
        conditions.append(Car.year_of_manufacture == year_of_manufacture)
    if brand:
        conditions.append(Car.brand == brand)

    cars = db.query(Car).filter(*conditions).all()
    return cars


@app.get("/orders_with_cars/", response_model=List[Order_response])
def get_orders_with_cars(db: Session = Depends(get_db)):
    orders = db.query(Order).join(Car).all()
    return orders


@app.put("/update_order_price/{order_id}", response_model=Order_response)
def update_order_price(order_id: int, new_price: int, db: Session = Depends(get_db)):
    stmt = update(Order).where(Order.id == order_id).values(price=new_price)
    db.execute(stmt)
    db.commit()
    updated_order = db.query(Order).filter(Order.id == order_id).first()
    return updated_order
