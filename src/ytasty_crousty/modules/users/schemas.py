from pydantic import BaseModel, ConfigDict, StringConstraints
from typing import Literal, Optional
from typing_extensions import Annotated

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9]{8,12}$")]
    password: Annotated[str, StringConstraints(pattern=r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{12,64}$")]
    role: Literal["admin", "staff", "direction"]
    restaurant_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    role: str
    restaurant_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)