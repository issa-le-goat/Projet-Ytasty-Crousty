from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# --- Import de la base de données ---
from ytasty_crousty.database import get_db

# --- Imports des Modèles et Schémas (à vérifier selon vos noms de classes exacts) ---
from ytasty_crousty.modules.restaurants.models import Restaurant
from ytasty_crousty.modules.restaurants.schemas import RestaurantResponse

from ytasty_crousty.modules.products.models import Product
from ytasty_crousty.modules.products.schemas import ProductResponse

from ytasty_crousty.modules.ordres.models import Order
from ytasty_crousty.modules.ordres.schemas import OrderResponse

# Initialisation du routeur
router = APIRouter(tags=["Gets"])


# ==========================================
# 0. Santé de l'API
# ==========================================
@router.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}


# ==========================================
# 3. RESTAURANTS
# ==========================================
@router.get("/restaurants", response_model=List[RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return restaurant


# ==========================================
# 4. PRODUITS / CARTE
# ==========================================
@router.get("/products", response_model=List[ProductResponse])
def get_products(
        category: Optional[str] = Query(None),
        q: Optional[str] = Query(None),
        restaurant_id: Optional[int] = Query(None),
        is_available: Optional[bool] = Query(None),
        db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    if restaurant_id is not None:
        query = query.filter(Product.restaurant_id == restaurant_id)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)

    return query.all()


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


# ==========================================
# 5. COMMANDES
# ==========================================
@router.get("/orders/{order_number}", response_model=OrderResponse)
def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.get("/restaurants/{restaurant_id}/orders", response_model=List[OrderResponse])
def get_restaurant_orders(
        restaurant_id: int,
        status: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    # Attention: Selon les consignes, cette route nécessite une authentification
    # et une vérification de rôle (staff du restaurant ou admin/direction).
    # Vous devrez ajouter votre Depends() d'authentification ici par la suite.
    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)

    if status:
        query = query.filter(Order.status == status)

    return query.all()