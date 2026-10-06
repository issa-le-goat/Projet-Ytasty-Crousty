from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from typing import Literal, List, Optional
from sqlalchemy.orm import Session

# ==========================================
# 1. IMPORTS DE LA BASE DE DONNÉES
# ==========================================
# Ces imports relient ce fichier à ta base de données générée par seed.py
from ytasty_crousty.database import SessionLocal, engine
from ytasty_crousty.modules.restaurants.models import Restaurant as DB_Restaurant
from ytasty_crousty.modules.products.models import Product as DB_Product

app = FastAPI()


# ==========================================
# 2. SCHÉMAS DE RÉPONSE (PYDANTIC)
# ==========================================
class OrderSchema(BaseModel):
    order_number: int
    restaurant_id: int
    created_at: str
    items: list[str]
    total_price: float
    status: Literal["pending", "validated", "preparing", "ready", "collected", "cancelled"]
    pickup_mode: Literal["onsite", "takeaway"]
    customer: str

    model_config = ConfigDict(from_attributes=True)


class RestaurantSchema(BaseModel):
    id: int
    name: str
    city: str
    address: str
    is_open: bool
    opening_hours: str | None = None
    contact: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(BaseModel):
    id: int
    name: str
    image: str | None = None
    description: str
    category: str
    price: float
    is_available: bool
    restaurant_id: int
    ingredients: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 3. DÉPENDANCE DE CONNEXION SQL
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 4. ROUTES DE L'API
# ==========================================

@app.get("/health", status_code=200)
def read_root():
    return {"status": "ok"}


@app.get("/restaurants", response_model=List[RestaurantSchema])
def get_restaurants(db: Session = Depends(get_db)):
    """Récupère la liste de tous les restaurants depuis la base de données"""
    return db.query(DB_Restaurant).all()


@app.get("/restaurants/{restaurant_id}", response_model=RestaurantSchema)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    """Récupère un restaurant spécifique grâce à son ID"""
    restaurant = db.query(DB_Restaurant).filter(DB_Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return restaurant


@app.get("/products", response_model=List[ProductSchema])
def get_products(restaurant_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Récupère les produits. Si restaurant_id est fourni, filtre les résultats."""
    query = db.query(DB_Product)

    # Filtre appliqué automatiquement si l'URL contient ?restaurant_id=...
    if restaurant_id is not None:
        query = query.filter(DB_Product.restaurant_id == restaurant_id)

    return query.all()


@app.get("/products/{product_id}", response_model=ProductSchema)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Récupère un produit spécifique grâce à son ID"""
    product = db.query(DB_Product).filter(DB_Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product