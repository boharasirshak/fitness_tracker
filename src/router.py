from .routes.operations import router as operations_router
from .routes.trains import router as trains_router
from .routes.auth import router as auth_router
from .routes.tokens import router as tokens_router
from .routes import setup_api_routes

__all__ = [
    "setup_api_routes",
    "operations_router", 
    "trains_router",
    "auth_router",
    "tokens_router",
]
