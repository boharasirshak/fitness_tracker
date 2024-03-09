from fastapi import FastAPI, APIRouter, Request, Depends

from src.config import templates
from .api.auth import router as auth_router
from .api.operations import router as operations_router
from .api.tokens import router as tokens_router
from .api.trains import router as trains_router

router = APIRouter(
    tags=["Pages"]
)

def setup_api_routes(app: FastAPI):
    app.include_router(
        auth_router, prefix = "/api/v1", tags = ['Auth']
    )

    app.include_router(
        operations_router, prefix ="/api/v1", tags = ['Operations']
    )
    
    app.include_router(
        tokens_router, prefix = "/api/v1", tags = ['Tokens']
    )
    
    app.include_router(
        trains_router, prefix = "/api/v1", tags = ['Trains']
    )

@router.get("/auth/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/auth/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
