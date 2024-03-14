from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.models.users import User
from app.core.database import get_db
from app.schemas import ErrorResponseSchema
from app.schemas.users import (
    UserDataAddSchema,
    UserDataSchema
)
from app.config import (
    access_security
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_description="Gets user's data",
    responses={
        200: {"model": UserDataSchema, "description": "Entire user's data"},
        401: {"model": ErrorResponseSchema, "description": "Token is invalid, expired or not provided"},
        404: {"model": ErrorResponseSchema, "description": "User not found"},
    }
)
async def get_user_data(
        db: AsyncSession = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security),
):
    # region TODO: make this a middleware
    user_id = credentials.subject.get("user_id")
    if not user_id or user_id == "":
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder({
                "detail": "Invalid token: user_id is missing in the subject"
            })
        )

    # check if user_id is integer
    try:
        user_id = int(user_id)
    except ValueError:
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder({
                "detail": "Invalid token: user_id is not an integer"
            })
        )
    # endregion

    async with db as session:
        # noinspection PyTypeChecker
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()

    if not user:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({
                "detail": "User not found"
            })
        )

    return UserDataSchema(
        email=user.email,
        username=user.username,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        activity_level=user.activity_level
    )
