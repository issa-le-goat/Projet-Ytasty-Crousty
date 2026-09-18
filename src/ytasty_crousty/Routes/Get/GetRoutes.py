from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel as BM
from typing import Literal, List, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()

engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Orders(BM):
    order_number: int
    restaurant_id: int
    created_at: str
    items: list[str]
    total_price: float
    status: Literal["pending", "validated", "preparing", "ready", "collected", "cancelled"]
    pickup_mode: Literal["onsite", "takeaway"]
    customer: str


class Restaurant(BM):
    id: int
    name: str
    city: str
    adress: str
    is_open: bool
    opening_hours: str
    contact: str

class Product(BM):
    id: int
    name: str
    image: str
    description: str
    category: str
    price: float
    is_available: bool
    restaurant_id: int
    ingredients: list[str]



@app.get("/health", status_code=200)
def read_root():
    return {"status": "ok"}


@app.get("/restaurants")
def get_Restaurants(restaurants: list[Restaurant]):
    return restaurants

@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_RestaurantsById(restaurant_id: int):
    return

@app.get("/products/{products_id}")
def get_productsById(products_id: int, product: Product):
    return product

@app.get("/products")
def get_products(products: list[Product]):
    return products

