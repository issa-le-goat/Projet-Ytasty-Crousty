from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

# Configuration des clés et algorithmes JWT
SECRET_KEY = "votre_cle_secrete_super_securisee"
ALGORITHM = "HS256"

# Configuration de passlib pour utiliser bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hache un mot de passe pour le sécuriser avec bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie que le mot de passe en clair correspond au mot de passe haché."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Génère le token JWT contenant les informations de l'utilisateur."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt