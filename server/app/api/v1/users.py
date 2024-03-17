import enum

from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.dependencies.jwt import jwt_verify
from app.models.users import User
from app.core.database import get_db
from app.schemas import ErrorResponseSchema
from app.schemas.users import (
    UserDataUpdateSchema,
    UserDataSchema
)
from app.config import (
    access_security
)

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get(
    "/me",
    response_description="Gets user's data",
    responses={
        200: {"model": UserDataSchema, "description": "Все данные пользователя"},
        401: {"model": ErrorResponseSchema, "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "Пользователь не найден"},
    }
)
async def get_user_data(
    user: User = Depends(jwt_verify)
):
    return UserDataSchema(
        email=user.email,
        username=user.username,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        activity_level=user.activity_level
    )


@router.put(
    "/",
    response_description="Обновляет данные пользователя",
    responses={
        200: {"model": UserDataSchema, "description": "Все обновленные данные пользователя"},
        401: {"model": ErrorResponseSchema, "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "Пользователь не найден"},
    }
)
async def change_user_data(
        data: UserDataUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(jwt_verify)
):
    async with db as session:
        # we create a new user object because the `user` we get from jwt_verify is not persistent in the session
        # noinspection PyTypeChecker
        query = select(User).where(User.id == user.id)
        result = await session.execute(query)
        new_user = result.scalar()

        update_data = data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            if isinstance(value, enum.Enum):
                value = value.value
            setattr(new_user, key, value)

        await session.commit()
        await session.refresh(new_user)

        return UserDataSchema(
            email=new_user.email,
            username=new_user.username,
            gender=new_user.gender,
            height=new_user.height,
            weight=new_user.weight,
            activity_level=new_user.activity_level
        )
