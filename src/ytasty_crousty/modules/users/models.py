import enum 

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ytasty_crousty.database import Base

class RoleEnum(str, enum.Enum):
    admin="admin"
    staff="staff"
    direction = "direction"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(12), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=True)

    restaurant = relationship("Restaurant", back_populates="users")