from fastapi import FastAPI

from .auth import router as auth_router
from .operations import router as operations_router
from .tokens import router as tokens_router
from .trains import router as trains_router

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
