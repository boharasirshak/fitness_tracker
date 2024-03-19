import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import BASE_URL
from app.core.emails import init_smtp
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tokens import router as tokens_router
from app.api.v1.exercises import router as exercises_router
from app.api.v1.workouts import router as workouts_router

from app.core.database import (
    create_tables,
    # drop_tables
)

logging.getLogger('passlib').setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Warning: This will drop all tables, so use only in dev
    # asyncio.create_task(drop_tables())
    asyncio.create_task(init_smtp())
    asyncio.create_task(create_tables())
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

if BASE_URL.__contains__("localhost"):
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['*'])
else:
    domain = BASE_URL.split("//")[1]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=[domain, f'*.{domain}'])

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def get_login_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/profile")
def get_login_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/workouts/new")
def get_login_page(request: Request):
    return templates.TemplateResponse("new-workouts.html", {"request": request})


app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tokens_router, prefix="/api/v1")
app.include_router(exercises_router, prefix="/api/v1")
app.include_router(workouts_router, prefix="/api/v1")
