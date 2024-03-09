from fastapi import FastAPI, APIRouter

from .routes.api.auth import router as auth_router
from .routes.api.operations import router as operations_router
from .routes.api.tokens import router as tokens_router
from .routes.api.trains import router as trains_router

router = APIRouter(
    tags=["Pages"]
)

def setup_api_routes(app: FastAPI):
    app.include_router(
        auth_router, prefix="/api/v1", tags=['Auth']
    )

    app.include_router(
        operations_router, prefix="/api/v1", tags=['Operations']
    )
    
    app.include_router(
        tokens_router, prefix="/api/v1", tags=['Tokens']
    )
    
    app.include_router(
        trains_router, prefix="/api/v1", tags=['Trains']
    )

__all__ = [
    "setup_api_routes",
    "setup_static_routes"
]
