import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tokens import router as tokens_router

from app.core.emails import init_smtp
from app.core.database import (
    create_tables,
    # drop_tables
)

logging.getLogger('passlib').setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Warning: This will drop all tables, so use only in dev
    # asyncio.create_task(drop_tables())
    asyncio.create_task(create_tables())
    asyncio.create_task(init_smtp())
    print("Setup SMTP and Database Tables Successful")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tokens_router, prefix="/api/v1")
