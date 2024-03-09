from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_jwt import JwtAuthorizationCredentials
from fastapi import APIRouter, Depends, Security

from src.database import get_db
from src.routes.api.auth.models import User
from src.config import access_security

router = APIRouter(prefix="/users")

@router.put("/add")
async def add_info(
    db: AsyncSession = Depends(get_db),
    access: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = access.payload.get("user_id")
    user = await db.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    
    return user
