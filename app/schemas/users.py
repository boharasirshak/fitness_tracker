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
    email: Optional[str] = None
    username: Optional[str] = None
    gender: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None

    # Throws an error if any extra fields are present
    class Config:
        extra = "forbid"


class UserDataSchema(BaseModel):
    email: str
    gender: str
    username: str
    height: int
    weight: int
    activity_level: ActivityLevel | int


class UserLoginResponseSchema(BaseModel):
    email: str
    access_token: str
    refresh_token: str
    username: str


class UserRegisterResponseSchema(BaseModel):
    message: str

