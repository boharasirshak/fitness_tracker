from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(BaseModel):
    email: str


class UserLoginResponseSchema(BaseModel):
    username: str
    email: str
    role_id: int
    access_token: str
    refresh_token: str


class UserRegisterResponseSchema(BaseModel):
    message: str


class AuthErrorResponseSchema(BaseModel):
    detail: str
