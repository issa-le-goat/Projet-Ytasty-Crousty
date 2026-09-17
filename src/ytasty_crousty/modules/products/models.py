from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, JSON
from sqlalchemy.orm import relationship

from ytasty_crousty.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    image = Column(String(500))
    description = Column(String)
    category = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    ingredients = Column(JSON)

    restaurant = relationship("Restaurant", back_populates="products")