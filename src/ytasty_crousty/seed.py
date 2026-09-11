from ytasty_crousty.database import SessionLocal, Base, engine

from modules.restaurants.models import Restaurant
from modules.users.models import User, RoleEnum
from modules.products.models import Product
from modules.ordres.models import Order, OrderItem
from modules.auths.security import pasword_hash

RESTAURANT_NAMES = [
    ("Ytasty Crousty Aix", "Aix-en-Provence"),
    ("Ytasty Crousty Paris", "Paris"),
    ("Ytasty Crousty Lyon", "Lyon"),
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
