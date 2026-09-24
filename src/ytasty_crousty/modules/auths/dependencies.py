from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from ytasty_crousty.database import SessionLocal # À adapter selon votre configuration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dépendance fictive à remplacer par votre logique de décodage JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 1. Décoder le token JWT
    # 2. Récupérer l'utilisateur en base
    # 3. Lancer HTTP 401 si invalide
    pass

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user = Depends(get_current_user)):
        if user.role.value not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Opération non autorisée pour ce rôle"
            )
        return user

allow_admin = RoleChecker(["admin"])
allow_staff_admin_direction = RoleChecker(["admin", "staff", "direction"])