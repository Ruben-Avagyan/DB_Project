import requests
import random
from faker import Faker
from database import Base, engine
from sqlalchemy.orm import sessionmaker


BASE_URL = 'http://127.0.0.1:8000'
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()


def Car_populate():
    url = f"{BASE_URL}/car/"
    data = {
    "year_of_manufacture": random.randint(1990, 2020),
    "number": random.randint(11111, 99999),
    "brand": fake.pystr(),
    "full_name": fake.name()
    }
    response = requests.post(url=url, json=data)
    return response.json()


def Order_populate():
    url = f"{BASE_URL}/order/"
    data = {
    "date_of_issue": fake.date_between(start_date='-30y', end_date='today').strftime("%Y-%m-%d"),
    "price": random.randint(400, 2000),
    "real_end_date": fake.date_between(start_date='-30y', end_date='today').strftime("%Y-%m-%d"),
    "planning_date_of_end": fake.date_between(start_date='-30y', end_date='today').strftime("%Y-%m-%d"),
    "type_of_work": fake.pystr()
    }
    response = requests.post(url=url, json=data)
    return response.json()


def Mechanic_populate():
    url = f"{BASE_URL}/mechanic/"
    data = {
    "full_name": fake.name(),
    "table_number": random.randint(1, 999),
    "experience": random.randint(1, 10),
    "rank": fake.pystr()    
    }
    response = requests.post(url=url, json=data)
    return response.json()


for _ in range(100):
    Car_populate()

for _ in range(100):
    Order_populate()

for _ in range(100):
    Mechanic_populate()    


