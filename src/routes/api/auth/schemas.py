from typing import Optional
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str
    
class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str

