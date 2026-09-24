from ytasty_crousty.database import SessionLocal, Base, engine

from ytasty_crousty.modules.restaurants.models import Restaurant
from ytasty_crousty.modules.users.models import User, RoleEnum
from ytasty_crousty.modules.products.models import Product
from ytasty_crousty.modules.ordres.models import Order, OrderItem
from ytasty_crousty.modules.auths.security import hash_password

RESTAURANT_DATA = [
    {"name": "Ytasty Crousty Aix", "city": "Aix-en-Provence", "address": "Adresse par défaut Aix"},
    {"name": "Ytasty Crousty Paris", "city": "Paris", "address": "Adresse par défaut Paris"},
    {"name": "Ytasty Crousty Lyon", "city": "Lyon", "address": "Adresse par défaut Lyon"},
]


def seed():
    print("Création des tables en base de données...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        if db.query(Restaurant).count() == 0:
            print("Insertion des restaurants...")
            for data in RESTAURANT_DATA:
                restaurant = Restaurant(
                    name=data["name"],
                    city=data["city"],
                    address=data["address"],
                    is_open=True,
                    opening_hours="11:00-22:00",
                    contact="0102030405",
                )
                db.add(restaurant)
            db.commit()

        existing_admin = db.query(User).filter(User.username == "admin123").first()
        if existing_admin is None:
            print("Création de l'administrateur système...")
            admin = User(
                first_name="Admin",
                last_name="Ytasty",
                username="admin123",
                hashed_password=hash_password("Admin@12345"),
                role=RoleEnum.admin,
            )
            db.add(admin)
            db.commit()

        print(
            f"Succès : {db.query(Restaurant).count()} restaurants et {db.query(User).count()} utilisateur(s) en base.")

    except Exception as e:
        db.rollback()
        print(f"Erreur lors de l'initialisation des données : {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()