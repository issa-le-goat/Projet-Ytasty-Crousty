from pydantic import BaseModel, ConfigDict
from typing import List

class ProductResponse(BaseModel):
    id: int
    name: str
    image: str
    description: str
    category: str
    price: float
    is_available: bool
    restaurant_id: int
    ingredients: List[str]

    model_config = ConfigDict(from_attributes=True)