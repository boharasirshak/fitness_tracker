import hashlib
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from fastapi_jwt import JwtAuthorizationCredentials
from fastapi import APIRouter, Depends, Security, Response

from src.database import get_db
from src.config import access_security, refresh_security
from .schemas import LoginSchema, RegisterSchema

from src.config import access_security, refresh_security
from .models import User

router = APIRouter(prefix="/auth")


@router.get("/getinfo")
async def get_info(
    db: AsyncSession = Depends(get_db),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.payload.get("user_id")
    user = await db.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    
    return user

@router.post("/login")
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    password = hashlib.sha256(data.password.encode()).hexdigest()

    query = await db.execute(
        select(User).where(
            User.email == data.email, User.hashed_password == password
        )
    )
    user = query.scalars().first()
    if not user:
        return Response(status_code=401, content=json.dumps({
            "error": "email or password incorrect"
        }))

    subject = {"email": user.email, "user_id": user.id, "role_id": user.role_id}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return {
        "message": "User login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/register")
async def register(data: RegisterSchema, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(User).where(User.username == data.username))
    user = query.scalars().first()
    if user:
        return {"error": "User already exists"}

    password = hashlib.sha256(data.password.encode()).hexdigest()
    user = User(
        username=data.username, email=data.email, hashed_password=password, role_id=1
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    subject = {"username": data.username, "user_id": user.id, "role_id": user.role_id}

    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return {
        "message": "User registered successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
