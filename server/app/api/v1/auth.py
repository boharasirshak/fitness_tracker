from aiosmtplib.errors import SMTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models.users import User
from app.core.database import get_db
from app.schemas import ErrorResponseSchema
from app.schemas.users import (
    UserLoginSchema,
    UserRegisterSchema,
    UserRegisterResponseSchema,
    UserLoginResponseSchema
)
from app.core.emails import (
    read_email_template,
    # send_mail_sync, 
    send_mail_async,
)
from app.core.utils import generate_random_password
from app.core.security import verify_password, get_password_hash
from app.config import (
    access_security,
    refresh_security,
    BASE_URL
)

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    "/login",
    response_description="Войдите в систему с помощью электронной почты и пароля",
    responses={
        200: {"model": UserLoginResponseSchema, "description": "Успешный вход пользователя в систему"},
        401: {"model": ErrorResponseSchema, "description": "Неверный адрес электронной почты или пароль"}
    }
)
async def login(data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    # noinspection PyTypeChecker
    query = select(User).where(User.email == data.email)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not verify_password(data.password, user.hashed_password):
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder({
                "detail": "Неверный адрес электронной почты или пароль"
            })
        )

    subject = {
        "email": user.email,
        "user_id": user.id
    }

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return UserLoginResponseSchema(
        username=user.username,
        email=user.email,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/register",
    response_description="Зарегистрируйте пользователя по электронной почте и отправьте временный пароль на это электронное письмо",
    responses={
        200: {"model": UserRegisterResponseSchema,
              "description": "Регистрация прошла успешно, пароль отправлен на электронную почту"},
        409: {"model": ErrorResponseSchema, "description": "Электронная почта уже существует"},
    }
)
async def register(data: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    # noinspection PyTypeChecker
    query = select(User).where(User.email == data.email)
    result = await db.execute(query)
    user = result.scalars().first()

    if user:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder({
                "detail": "Электронная почта уже существует"
            })
        )

    temp_password = generate_random_password(20)
    hashed_password = get_password_hash(temp_password)

    html = read_email_template("temporary-password.html")
    html = html.replace("{{email}}", data.email)
    html = html.replace("{{temporary_password}}", temp_password)
    html = html.replace("{{login_url}}", f"{BASE_URL}/login")

    try:
        await send_mail_async(
            to=data.email,
            subject="Ваш временный пароль",
            html=html
        )

        # first send the email, then only register the user.
        user = User(email=data.email, hashed_password=hashed_password)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    except SMTPException as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({
                "detail": "Сообщение об ошибке при отправке на этот адрес электронной почты!"
            })
        )

    return UserRegisterResponseSchema(
        message="Временные данные отправлены на ваш электронный адрес."
    )
