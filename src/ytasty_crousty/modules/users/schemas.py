import re
from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from typing import Literal, Optional
from typing_extensions import Annotated


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    # Le nom d'utilisateur n'utilise pas de look-ahead, StringConstraints fonctionne ici
    username: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9]{8,12}$")]
    password: str
    role: Literal["admin", "staff", "direction"]
    restaurant_id: Optional[int] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Utilisation du module re de Python qui supporte les look-aheads
        pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{12,64}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Le mot de passe doit contenir entre 12 et 64 caractères, "
                "dont au moins une majuscule, un chiffre et un caractère spécial."
            )
        return v


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    role: str
    restaurant_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)