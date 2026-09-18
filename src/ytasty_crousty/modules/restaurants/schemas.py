from pydantic import BaseModel, ConfigDict

class RestaurantResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str
    is_open: bool
    opening_hours: str
    contact: str

    # Permet de convertir l'objet SQLAlchemy en JSON
    model_config = ConfigDict(from_attributes=True)