from pydantic import BaseModel, Field, ConfigDict, StringConstraints
from typing import List, Literal, Optional

class RestaurantResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str
    is_open: bool
    opening_hours: str
    contact: str

class RestaurantUpdate(BaseModel):
    address: Optional[str] = None
    contact: Optional[str] = None

class RestaurantAvailability(BaseModel):
    is_open: bool

    # Permet de convertir l'objet SQLAlchemy en JSON
    model_config = ConfigDict(from_attributes=True)