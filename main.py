from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.database import Base
from src.database import engine
from src.router import setup_api_routes

load_dotenv()
app = FastAPI()
lifespan = app.router.lifespan_context
templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@asynccontextmanager
async def lifespan_wrapper(app):
    print("Starting the app")
    async with engine.begin() as conn:
        # await conn.run_sync(
        #     Base.metadata.drop_all
        # )  # drop all tables
        await conn.run_sync(Base.metadata.create_all)

    async with lifespan(app) as state:
        yield state

    print("Sutting down the app")


app.router.lifespan_context = lifespan_wrapper

setup_api_routes(app)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/auth/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="00.0.0.0", port=8000)
