import enum

from pydantic import BaseModel


class ActivityLevel(enum.Enum):
    not_given = 0   # Value not given during registration
    beginner = 1    # Doesn't practice much
    average = 2     # Practice sports 1-3 timer per week
    athlete = 3     # Practice sports 3-5 times per week
    # add more activity levels here


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(BaseModel):
    email: str


class UserDataAddSchema(BaseModel):
    username: str
    height: int
    weight: int
    activity_level: ActivityLevel


class UserDataSchema(BaseModel):
    email: str
    gender: str
    username: str
    height: int
    weight: int
    activity_level: ActivityLevel


class UserLoginResponseSchema(BaseModel):
    email: str
    access_token: str
    refresh_token: str
    username: str


class UserRegisterResponseSchema(BaseModel):
    message: str

