from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    email: str


class UserLoginResponseSchema(BaseModel):
    username: str
    email: str
    role_id: int
    access_token: str
    refresh_token: str


class UserRegisterResponseSchema(BaseModel):
    username: str
    email: str
    role_id: int
    access_token: str
    refresh_token: str


class AuthErrorResponseSchema(BaseModel):
    error: str
