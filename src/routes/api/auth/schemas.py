from typing import Optional
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str
    
class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str


class UserRead(BaseModel):
    id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    role_id: Optional[int]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        orm_mode = True

