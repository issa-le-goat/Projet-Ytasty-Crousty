from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ytasty_crousty.database import get_db
from ytasty_crousty.modules.users.models import User
from ytasty_crousty.modules.auths.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session.Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    user = db.query(User).fiter(User.username == username).first()
    if user is none:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")

    return user

# Mis en commentaire car apparaitra possiblement autre part dans le projet mais reste ici comme sauvegarde
'''
def require_role(*allowed_roles: str):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value not in allowed_roles:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        return current_user
    return role checker
'''