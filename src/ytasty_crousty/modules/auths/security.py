from passlib.context import CryptContext
from pydantic import BaseModel, Field
from typing import List, Literal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Hash un mot de passe pour le sécuriser
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Vérifie que le mot de passe hacher correspond au mot de passe non-haché
    return pwd_context.verify(plain_password, hashed_password)

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0) # Contrainte: quantité > 0

class CustomerCreate(BaseModel):
    name: str
    email: str

class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]
    pickup_mode: Literal["onsite", "takeaway"]
    customer: CustomerCreate

class OrderStatusUpdate(BaseModel):
    status: Literal["pending", "validated", "preparing", "ready", "collected", "cancelled"]