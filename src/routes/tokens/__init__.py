from datetime import timedelta

from fastapi import APIRouter, Security
from fastapi_jwt import JwtAuthorizationCredentials

from src.config import (
    access_security, 
    refresh_security, 
    REFRESH_TOKEN_EXPIRATION
)

router = APIRouter(prefix="/tokens")

@router.post("/verify")
async def verify_token(credentials: JwtAuthorizationCredentials = Security(access_security)):
    return {"message": "Token is valid"}


@router.get("/refresh")
async def refresh_token(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(
        subject=credentials.subject,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRATION),
    )

    return {"access_token": access_token, "refresh_token": refresh_token}
