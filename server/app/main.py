import json
import asyncio
import logging
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload

# from app.core.emails import init_smtp
from app.models import Workout, WorkoutExercise, User
from app.schemas.workouts import workout_to_schema
from app.core.utils import insert_default_data
from app.core.security import is_valid_jwt

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tokens import router as tokens_router
from app.api.v1.exercises import router as exercises_router
from app.api.v1.websockets import router as websockets_router
from app.api.v1.workouts import router as workouts_router

from app.core.database import create_tables, drop_tables, get_db
from app.schemas.users import UserSchema

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
    # return templates.TemplateResponse("index.html", {"request": request})
    return RedirectResponse("/login")


@app.get("/register")
def register_page(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token and is_valid_jwt(access_token):
        return RedirectResponse(url="/dashboard")

    response = templates.TemplateResponse(
        "register.html",
        {
            "request": request,
        },
    )
    if access_token:
        response.delete_cookie("access_token")

    return response


@app.get("/login")
def login_page(request: Request):
    access_token = request.cookies.get("access_token")

    if access_token and is_valid_jwt(access_token):
        return RedirectResponse(url="/dashboard")

    response = templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )
    if access_token:
        response.delete_cookie("access_token")

    return response


@app.get("/dashboard")
async def dashboard_page(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return RedirectResponse(url="/login")

    token = is_valid_jwt(access_token)

    if not token or token.get("subject", {}).get("user_id") is None:
        resp = RedirectResponse(url="/login")
        resp.delete_cookie("access_token")
        return resp

    query = (
        select(Workout)
        .where(Workout.user_id == token["subject"]["user_id"])
        .options(
            joinedload(Workout.user),
            joinedload(Workout.workout_exercises).joinedload(WorkoutExercise.exercise),
            joinedload(Workout.workout_exercises).joinedload(
                WorkoutExercise.workout_sessions
            ),
        )
    )

    workouts = []
    result = await db.execute(query)
    data = result.unique().scalars().all()

    for workout in data:
        workouts.append(json.loads(workout_to_schema(workout).model_dump_json()))

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "access_token": access_token,
            "workouts": workouts,
        },
    )


@app.get("/profile")
async def profile_page(request: Request, db: AsyncSession = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return RedirectResponse(url="/login")

    token = is_valid_jwt(access_token)

    if not token or token.get("subject", {}).get("user_id") is None:
        resp = RedirectResponse(url="/login")
        resp.delete_cookie("access_token")
        return resp

    query = select(User).where(User.id == token["subject"]["user_id"])
    result = await db.execute(query)
    user = result.scalar()

    if not user:
        resp = RedirectResponse(url="/login")
        resp.delete_cookie("access_token")
        return resp

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "access_token": access_token,
            "user": UserSchema(
                email=user.email,
                name=user.name,
                gender=user.gender,
                height=user.height,
                weight=user.weight,
                activity_level=user.activity_level,
                profile_picture_url=user.profile_picture_url or "",
                age=user.age,
                desired_weight=user.desired_weight,
            ),
        },
    )


# @app.get("/workouts/")
# def new_workout(request: Request):
#     access_token = request.cookies.get("access_token", None)
#     return templates.TemplateResponse(
#         "workouts.html", {"request": request, "access_token": access_token}
#     )


# @app.get("/workouts/new")
# def new_workout(request: Request):
#     access_token = request.cookies.get("access_token", None)
#     return templates.TemplateResponse("new-workout.html.html", {"request": request, "access_token": access_token})


# @app.get("/workouts/start/{workout_id}")
# def start_workout(
#     workout_id: int, request: Request, workout: Workout = Depends(workout_verify)
# ):
#     return templates.TemplateResponse(
#         "workout.html", {"request": request, "workout": workout}
#     )


app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tokens_router, prefix="/api/v1")
app.include_router(exercises_router, prefix="/api/v1")
app.include_router(websockets_router, prefix="/api/v1")
app.include_router(workouts_router, prefix="/api/v1")
