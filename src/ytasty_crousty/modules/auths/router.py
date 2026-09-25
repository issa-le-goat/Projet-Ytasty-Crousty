from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import timedelta

from ytasty_crousty.database import get_db
from ytasty_crousty.modules.users.models import User
from ytasty_crousty.modules.auths.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 60


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Recherche de l'utilisateur
    user = db.query(User).filter(User.username == credentials.username).first()

    # 2. Vérification de l'identifiant et du mot de passe
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiant ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Génération du token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Gestion de l'Enumération pour le rôle
    role_value = user.role.value if hasattr(user.role, 'value') else user.role

    access_token = create_access_token(
        data={"sub": user.username, "role": role_value, "restaurant_id": user.restaurant_id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
