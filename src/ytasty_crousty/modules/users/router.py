from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib

from ytasty_crousty.database import get_db
from ytasty_crousty.modules.users.models import User
from ytasty_crousty.modules.users.schemas import UserCreate, UserResponse
from ytasty_crousty.modules.auths.dependencies import allow_admin

router = APIRouter(prefix="/users", tags=["Users"])


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_admin=Depends(allow_admin)
):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Cet identifiant existe déjà.")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        hashed_password=hash_password(user.password),
        role=user.role,
        restaurant_id=user.restaurant_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user