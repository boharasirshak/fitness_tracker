import enum
import os
import shutil
import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, UploadFile, File
from starlette.responses import JSONResponse

from app.dependencies.jwt import jwt_verify
from app.models.users import User
from app.core.database import get_db
from app.schemas import ErrorResponseSchema
from app.schemas.users import (
    UserDataUpdateSchema,
    UserSchema,
    FileUploadResponseSchema
)

router = APIRouter(prefix="/users", tags=["Пользователи"])
UPLOAD_DIRECTORY = "app/static/uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.get(
    "/me",
    response_description="Получает данные пользователя",
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
        phone_number=user.phone_number or "",
        profile_picture_url=user.profile_picture_url or ""
    )


@router.put(
    "", # You might be temped to add a '/' here, but don't do it because it redirects traffics. Apparently FastAPI and NGINX redrections are clashing with each other.
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


@router.put(
    "/photo",
    response_description="Обновляет фото пользователя",
    responses={
        200: {"model": FileUploadResponseSchema, "description": "Successfully uploaded and saved a file"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        409: {"model": ErrorResponseSchema, "description": "Invalid file type"},
    }
)
async def change_user_picture(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(jwt_verify),
    photo: UploadFile = File(...)
):
    extension = photo.filename.split(".")[-1]
    if extension not in ["jpg", "jpeg", "png"]:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder({
                "detail": "Valid extensions are jpg, jpeg, png only!"
            })
        )

    filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    if user.profile_picture_url and os.path.exists(os.path.join(UPLOAD_DIRECTORY, user.profile_picture_url)):
        os.remove(os.path.join(UPLOAD_DIRECTORY, user.profile_picture_url))

    user.profile_picture_url = filename
    await db.commit()
    await db.refresh(user)

    return FileUploadResponseSchema(
        file_id=filename
    )
