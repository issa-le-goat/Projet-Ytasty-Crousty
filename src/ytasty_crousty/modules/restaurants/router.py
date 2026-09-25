from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ytasty_crousty.database import get_db
from ytasty_crousty.modules.restaurants.models import Restaurant
from ytasty_crousty.modules.restaurants.schemas import RestaurantResponse, RestaurantUpdate, RestaurantAvailability
from ytasty_crousty.modules.auths.dependencies import allow_admin

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("", response_model=List[RestaurantResponse], status_code=status.HTTP_200_OK)
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()


@router.get("/{restaurant_id}", response_model=RestaurantResponse, status_code=status.HTTP_200_OK)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant introuvable.")
    return restaurant


@router.patch("/{restaurant_id}", response_model=RestaurantResponse, status_code=status.HTTP_200_OK)
def update_restaurant(
        restaurant_id: int,
        data: RestaurantUpdate,
        db: Session = Depends(get_db),
        current_admin=Depends(allow_admin)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant introuvable.")

    if data.address is not None:
        restaurant.address = data.address
    if data.contact is not None:
        restaurant.contact = data.contact

    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.patch("/{restaurant_id}/availability", response_model=RestaurantResponse, status_code=status.HTTP_200_OK)
def update_availability(
        restaurant_id: int,
        data: RestaurantAvailability,
        db: Session = Depends(get_db),
        current_admin=Depends(allow_admin)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant introuvable.")

    restaurant.is_open = data.is_open
    db.commit()
    db.refresh(restaurant)
    return restaurant