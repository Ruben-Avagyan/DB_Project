from datetime import date
from pydantic import BaseModel
from models import Car, Mechanic, Order
from database import Base, engine, SessionLocal
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session


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


@app.post("/machanic/", response_model=mechanic_response)
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