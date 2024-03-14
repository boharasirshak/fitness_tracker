from pydantic import BaseModel


class TokenVerifyResponse(BaseModel):
    message: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
