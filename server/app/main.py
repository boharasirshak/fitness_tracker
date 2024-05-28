import asyncio
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# from app.core.emails import init_smtp
from app.models.workouts import Workout
from app.core.utils import insert_default_data
from app.dependencies.workouts import workout_verify

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tokens import router as tokens_router
from app.api.v1.exercises import router as exercises_router
from app.api.v1.websockets import router as websockets_router
from app.api.v1.workouts import router as workouts_router

from app.core.database import create_tables, drop_tables

logging.getLogger("passlib").setLevel(logging.ERROR)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Warning: This will drop all tables, so use only in dev
    # asyncio.create_task(init_smtp())
    # asyncio.create_task(drop_tables())
    asyncio.create_task(create_tables())
    asyncio.create_task(insert_default_data())
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/profile")
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/workouts/")
def new_workout(request: Request):
    return templates.TemplateResponse("workouts.html", {"request": request})


@app.get("/workouts/new")
def new_workout(request: Request):
    return templates.TemplateResponse("new-workout.html", {"request": request})


@app.get("/workouts/start/{workout_id}")
def start_workout(
    workout_id: int, request: Request, workout: Workout = Depends(workout_verify)
):
    return templates.TemplateResponse(
        "workout.html", {"request": request, "workout": workout}
    )


app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tokens_router, prefix="/api/v1")
app.include_router(exercises_router, prefix="/api/v1")
app.include_router(websockets_router, prefix="/api/v1")
app.include_router(workouts_router, prefix="/api/v1")
