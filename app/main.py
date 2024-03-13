import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.auth import router as auth_router
from app.core.emails import init_smtp
from app.core.database import create_tables, drop_tables

logging.getLogger('passlib').setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warning: This will drop all tables, so use only in dev
    # asyncio.create_task(drop_tables())
    asyncio.create_task(create_tables())
    asyncio.create_task(init_smtp())
    print("Setup SMTP and Database Tables Successful")
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(auth_router, prefix="/api/v1")
