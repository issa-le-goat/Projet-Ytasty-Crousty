from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ytasty_crousty.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    is_open = Column(Boolean, default=True)
    opening_hours = Column(String(255))
    contact = Column(String(50))

    #permet de faire restaurant.products, restaurant.users, restaurant.orders
    products = relationship("Product", back_populates="restaurant")
    users = relationship("User", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")