import enum
from typing import Optional

from pydantic import BaseModel

from app.models.users import ActivityLevel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(BaseModel):
    email: str


class UserDataUpdateSchema(BaseModel):
    username: Optional[str] = None
    gender: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None

    # Throws an error if any extra fields are present
    class Config:
        extra = "forbid"


class UserSchema(BaseModel):
    email: str
    gender: str
    username: str
    height: int
    weight: int
    activity_level: ActivityLevel | int
    phone_number: str


class UserLoginResponseSchema(BaseModel):
    email: str
    access_token: str
    refresh_token: str
    username: str


class UserRegisterResponseSchema(BaseModel):
    message: str

