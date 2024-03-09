from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.database import Base
from src.database import engine
from src.router import setup_api_routes

load_dotenv()
app = FastAPI()
lifespan = app.router.lifespan_context


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
async def index():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    uvicorn.run(app, host="00.0.0.0", port=8000)