import sys
import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Configuration du PATH
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_path not in sys.path:
    sys.path.append(src_path)

from ytasty_crousty.database import SessionLocal, Base, engine
from ytasty_crousty.modules.restaurants.models import Restaurant
from ytasty_crousty.modules.users.models import User, RoleEnum
from ytasty_crousty.modules.products.models import Product
from ytasty_crousty.modules.ordres.models import Order

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Création des restaurants
        restaurants_data = [
            {"name": "Ytasty Crousty Aix", "city": "Aix-en-Provence", "address": "123 Cours Mirabeau", "is_open": True},
            {"name": "Ytasty Crousty Paris", "city": "Paris", "address": "45 Avenue des Champs-Élysées",
             "is_open": True},
            {"name": "Ytasty Crousty Lyon", "city": "Lyon", "address": "8 Place Bellecour", "is_open": True}
        ]

        created_restaurants = []
        for r_data in restaurants_data:
            restaurant = db.query(Restaurant).filter(Restaurant.name == r_data["name"]).first()
            if not restaurant:
                restaurant = Restaurant(**r_data)
                db.add(restaurant)
                db.flush()  # Permet de générer l'ID du restaurant immédiatement
            created_restaurants.append(restaurant)

        # 2. Création des produits (Catalogue de base)
        # Attention : adapte les clés (name, description...) selon les noms exacts des colonnes de ton Product
        products_template = [
            {
                "name": "Le Classic Crousty",
                "image": "classic_crousty.jpg",
                "description": "Burger authentique avec bœuf haché, cheddar fondu et sauce maison.",
                "category": "Burger",
                "price": 8.90,
                "is_available": True,
                "ingredients": "Pain sésame, Steak haché 150g, Cheddar affiné, Salade, Tomate, Oignon rouge, Sauce Crousty"
            },
            {
                "name": "Chicken Crispy Supreme",
                "image": "chicken_crispy.jpg",
                "description": "Filet de poulet pané ultra croustillant, bacon et sauce barbecue.",
                "category": "Burger",
                "price": 10.50,
                "is_available": True,
                "ingredients": "Pain brioché, Poulet croustillant, Bacon fumé, Cheddar, Salade, Sauce BBQ"
            },
            {
                "name": "Frites Maison",
                "image": "frites.jpg",
                "description": "Pommes de terre fraîches coupées sur place et cuites en double bain.",
                "category": "Accompagnement",
                "price": 3.50,
                "is_available": True,
                "ingredients": "Pommes de terre bintje, Sel de Guérande"
            },
            {
                "name": "Coca-Cola Zero",
                "image": "coca_zero.jpg",
                "description": "Boisson rafraîchissante sans sucres.",
                "category": "Boisson",
                "price": 2.50,
                "is_available": True,
                "ingredients": "Eau gazéifiée, colorant, acidifiants, édulcorants"
            }
        ]

        # 3. Affectation des produits à chaque restaurant
        for restaurant in created_restaurants:
            for p_data in products_template:
                # Vérifie si le produit existe déjà pour ce restaurant
                existing_product = db.query(Product).filter(
                    Product.name == p_data["name"],
                    Product.restaurant_id == restaurant.id
                ).first()

                if not existing_product:
                    # Copie du template et ajout de l'ID du restaurant
                    new_product_data = p_data.copy()
                    new_product_data["restaurant_id"] = restaurant.id

                    product = Product(**new_product_data)
                    db.add(product)

        # 4. Création du compte administrateur
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if not existing_admin:
            admin_user = User(
                first_name="Admin",
                last_name="System",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role=RoleEnum.admin
            )
            db.add(admin_user)

        db.commit()
        print("Les données (Restaurants, Produits et Admin) ont été injectées avec succès.")

    except Exception as e:
        db.rollback()
        print(f"Une erreur est survenue : {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()