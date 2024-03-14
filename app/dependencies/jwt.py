from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Depends, Request
from fastapi_jwt import JwtAuthorizationCredentials

from app.models.users import User
from app.core.database import get_db
from app.config import access_security


async def jwt_verify(
        _: Request,
        credentials: JwtAuthorizationCredentials = Depends(access_security),
        db: AsyncSession = Depends(get_db)
) -> User:
    user_id = credentials.subject.get("user_id")
    if not user_id or user_id == "":
        raise HTTPException(status_code=401, detail="Invalid token: user_id is missing in the subject")

    # Check if user_id is integer
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token: user_id is not an integer")

    # Here you could add more checks, e.g., verify user exists in DB
    async with db as session:
        # noinspection PyTypeChecker
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
