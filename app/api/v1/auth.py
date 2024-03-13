from aiosmtplib.errors import SMTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models.users import User
from app.core.database import get_db
from app.schemas.auth import (
    UserLoginSchema,
    UserRegisterSchema,
    UserRegisterResponseSchema,
    UserLoginResponseSchema,
    AuthErrorResponseSchema
)
from app.core.emails import read_email_template, send_mail_async
from app.core.utils import generate_random_password
from app.core.security import verify_password, get_password_hash
from app.config import (
    access_security,
    refresh_security,
    BASE_URL
)

router = APIRouter(prefix="/auth")


@router.post(
    "/login",
    response_description="Login user by email and password",
    responses={
        200: {"model": UserLoginResponseSchema, "description": "User login successful"},
        401: {"model": AuthErrorResponseSchema, "description": "Incorrect email or password"},
        500: {"model": AuthErrorResponseSchema, "description": "Internal server error"},
    }
)
async def login(data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    async with db as session:
        # noinspection PyTypeChecker
        query = select(User).where(User.email == data.email)
        result = await session.execute(query)
        user = result.scalars().first()

    if not user or not verify_password(data.password, user.hashed_password):
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder({
                "detail": "Incorrect email or password"
            })
        )

    subject = {
        "username": user.username,
        "email": user.email,
        "user_id": user.id,
        "role_id": user.role_id
    }

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return UserLoginResponseSchema(
        username=user.username,
        email=user.email,
        role_id=user.role_id,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/register",
    response_description="Register the user by email and send temporary password to that email",
    responses={
        200: {"model": UserRegisterResponseSchema, "description": "Registration successful & password sent to email"},
        409: {"model": AuthErrorResponseSchema, "description": "Email already exists"},
        500: {"model": AuthErrorResponseSchema, "description": "Internal server error"},
    }
)
async def register(data: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    async with db as session:
        # noinspection PyTypeChecker
        query = select(User).where(User.email == data.email)
        result = await session.execute(query)
        user = result.scalars().first()

    if user:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder({
                "detail": "Email already exists"
            })
        )

    temp_password = generate_random_password(12)
    hashed_password = get_password_hash(temp_password)

    user = User(email=data.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    html = read_email_template("temporary-password.html")
    html = html.replace("{{email}}", data.email)
    html = html.replace("{{temporary_password}}", temp_password)
    html = html.replace("{{login_url}}", f"{BASE_URL}/login")

    try:
        await send_mail_async(
            to=data.email,
            subject="Your Temporary Password",
            html=html
        )
    except SMTPException:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({
                "detail": "Error sending email to this email!"
            })
        )

    return UserRegisterResponseSchema(
        message="Temporary email sent to your email."
    )
