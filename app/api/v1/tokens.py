
from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt import JwtAuthorizationCredentials

from app.schemas import ErrorResponseSchema
from app.schemas.tokens import (
    TokenVerifyResponse,
    RefreshTokenResponse
)
from app.config import (
    access_security,
    refresh_security
)

router = APIRouter(prefix="/tokens", tags=["Tokens"])


@router.get(
    "/verify",
    description="Verifies if the token is valid",
    responses={
        200: {"model": TokenVerifyResponse, "description": "Token is valid"},
        401: {"model": ErrorResponseSchema, "description": "Token is invalid, expired or not provided"}
    }
)
async def verify_token(
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "message": "Token is valid"
        })
    )


@router.get(
    "/refresh",
    description="Refreshes the access token",
    responses={
        200: {"model": RefreshTokenResponse, "description": "Token is refreshed"},
        401: {"model": ErrorResponseSchema, "description": "Token is invalid, expired or not provided"}
    }
)
async def refresh_a_token(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)

    return JSONResponse(
        status_code=201,
        content=jsonable_encoder({
            "access_token": access_token,
            "refresh_token": refresh_token,
        })
    )
