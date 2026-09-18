from pydantic import BaseModel, ConfigDict
from typing import List, Literal
from datetime import datetime

# Sous-schéma pour un article de la commande
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int

# Sous-schéma pour le client
class CustomerResponse(BaseModel):
    name: str
    email: str

# Schéma principal de la commande
class OrderResponse(BaseModel):
    order_number: str
    restaurant_id: int
    created_at: datetime
    items: List[OrderItemResponse]
    total_price: float
    status: Literal["pending", "validated", "preparing", "ready", "collected", "cancelled"]
    pickup_mode: Literal["onsite", "takeaway"]
    customer: CustomerResponse

    model_config = ConfigDict(from_attributes=True)