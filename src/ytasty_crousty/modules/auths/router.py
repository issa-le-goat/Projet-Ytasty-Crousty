from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ytasty_crousty.database import get_db
from ytasty_crousty.modules.users.models import User
from ytasty_crousty.modules.auths.security import verify_password
from ytasty_crousty.modules.auths.jwt import create_access_token
from ytasty_crousty.modules.auths.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token(username=user.username, role=user.role.value)
    return TokenResponse(access_token=token)