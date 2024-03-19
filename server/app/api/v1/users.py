import enum

from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from app.dependencies.jwt import jwt_verify
from app.models.users import User
from app.core.database import get_db
from app.schemas import ErrorResponseSchema
from app.schemas.users import (
    UserDataUpdateSchema,
    UserSchema
)

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get(
    "/me",
    response_description="Gets user's data",
    responses={
        200: {"model": UserSchema, "description": "Все данные пользователя"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "Пользователь не найден"},
    }
)
async def get_user_data(
    user: User = Depends(jwt_verify)
):
    return UserSchema(
        email=user.email,
        username=user.username,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        activity_level=user.activity_level,
        phone_number=user.phone_number or ""
    )


@router.put(
    "",
    response_description="Обновляет данные пользователя",
    responses={
        200: {"model": UserSchema, "description": "Все обновленные данные пользователя"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "Пользователь не найден"},
    }
)
async def change_user_data(
        data: UserDataUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(jwt_verify)
):
    # noinspection PyTypeChecker
    query = select(User).where(User.id == user.id)
    result = await db.execute(query)
    new_user = result.scalar()

    update_data = data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        if isinstance(value, enum.Enum):
            value = value.value
        setattr(new_user, key, value)

    await db.commit()
    await db.refresh(new_user)

    return UserSchema(
        email=new_user.email,
        username=new_user.username,
        gender=new_user.gender,
        height=new_user.height,
        weight=new_user.weight,
        activity_level=new_user.activity_level,
        phone_number=new_user.phone_number
    )
