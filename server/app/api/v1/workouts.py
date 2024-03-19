from sqlalchemy.sql import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.dependencies.jwt import jwt_verify
from app.models import Exercise
from app.models.users import User
from app.models.workouts import Workout
from app.models.work_session import WorkoutSession
from app.core.database import get_db
from app.schemas import ErrorResponseSchema
from app.schemas.workouts import (
    AllWorkoutsSchema,
    DetailedWorkoutSchema,
    WorkoutSchema,
    WorkoutSessionSchema,
    CreateWorkoutSchema,
    CreateWorkoutResponseSchema,
    CreateWorkoutSessionSchema,
    CreateWorkoutSessionResponseSchema,
    ExerciseSchema
)

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get(
    "/",
    response_description="Gets all workouts done by users along with each session",
    responses={
        200: {"model": AllWorkoutsSchema, "description": "Все данные пользователя"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "User or Exercise not found"},
    }
)
async def get_all_users_workouts(
    user: User = Depends(jwt_verify),
    db: AsyncSession = Depends(get_db)
):
    all_workouts: list[DetailedWorkoutSchema] = []

    # noinspection PyTypeChecker
    query = select(Workout).where(Workout.user_id == user.id)
    result = await db.execute(query)
    workouts = result.scalars().all()
    if not workouts:
        return AllWorkoutsSchema(workouts=[])

    for workout in workouts:
        # noinspection PyTypeChecker, DuplicatedCode
        query = select(Exercise).where(Exercise.id == workout.exercise_id)
        result = await db.execute(query)
        exercise = result.scalars().first()

        if not exercise:
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({
                    "detail": "An exercise not found"
                })
            )

        workout_exercise = ExerciseSchema(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            created_at=exercise.created_at,
            video_link=exercise.video_link
        )

        # noinspection PyTypeChecker
        query = select(WorkoutSession).where(and_(
            WorkoutSession.workout_id == workout.id,
            WorkoutSession.user_id == user.id
        ))
        result = await db.execute(query)
        sessions = result.scalars().all()
        workout_sessions: list[WorkoutSessionSchema] = []

        for session in sessions:
            workout_sessions.append(WorkoutSessionSchema(
                id=session.id,
                user_id=session.user_id,
                workout_id=session.workout_id,
                start_time=session.start_time,
                end_time=session.end_time,
                repetitions=session.repetitions
            ))

        all_workouts.append(DetailedWorkoutSchema(
            id=workout.id,
            name=workout.name,
            description=workout.description,
            total_time=workout.total_time,
            rest_time=workout.rest_time,
            efficiency=workout.efficiency,
            user_id=workout.user_id,
            exercise_id=workout.exercise_id,
            created_at=workout.created_at,
            sessions=workout_sessions,
            exercise=workout_exercise
        ))

    return AllWorkoutsSchema(workouts=all_workouts)


@router.get(
    "/{workout_id}", 
    response_description="Get a single workout by its ID",
    responses={
        200: {"model": DetailedWorkoutSchema, "description": "Detailed workout schema"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "User or Exercise not found"},
    }
)
async def get_single_workout(
    workout_id: int, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(jwt_verify)
):
    # noinspection PyTypeChecker
    query = select(Workout).where(and_(
        Workout.id == workout_id,
        Workout.user_id == user.id
    ))
    result = await db.execute(query)
    workout = result.scalars().first()

    if not workout:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({
                "detail": "Workout not found"
            })
        )

    # noinspection PyTypeChecker
    query = select(Exercise).where(Exercise.id == workout.exercise_id)
    result = await db.execute(query)
    exercise = result.scalars().first()

    if not exercise:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({
                "detail": "Exercise not found"
            })
        )

    workout_exercise = ExerciseSchema(
        id=exercise.id,
        name=exercise.name,
        description=exercise.description,
        created_at=exercise.created_at,
        video_link=exercise.video_link
    )

    # noinspection PyTypeChecker
    query = select(WorkoutSession).where(WorkoutSession.workout_id == workout.id)
    result = await db.execute(query)
    sessions = result.scalars().all()
    workout_sessions: list[WorkoutSessionSchema] = []

    for session in sessions:
        workout_sessions.append(WorkoutSessionSchema(
            id=session.id,
            user_id=session.user_id,
            workout_id=session.workout_id,
            start_time=session.start_time,
            end_time=session.end_time,
            repetitions=session.repetitions
        ))

    return DetailedWorkoutSchema(
        id=workout.id,
        name=workout.name,
        description=workout.description,
        total_time=workout.total_time,
        rest_time=workout.rest_time,
        efficiency=workout.efficiency,
        user_id=workout.user_id,
        exercise_id=workout.exercise_id,
        created_at=workout.created_at,
        sessions=workout_sessions,
        exercise=workout_exercise
    )

@router.post(
    "/",
    response_description="Create a new workout for the user",
    responses={
        200: {"model": CreateWorkoutResponseSchema, "description": "A new workout created"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "User or exercise not found"},
    }
)
async def create_new_workout(
    data: CreateWorkoutSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(jwt_verify)
):
    # noinspection PyTypeChecker
    query = select(Exercise).where(Exercise.id == data.exercise_id)
    result = await db.execute(query)
    exercise = result.scalars().first()

    if not exercise:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({
                "detail": "Exercise not found"
            })
        )

    new_workout = Workout(
        name=data.name,
        description=data.description,
        total_time=data.total_time,
        rest_time=data.rest_time,
        user_id=user.id,
        exercise_id=data.exercise_id
    )

    db.add(new_workout)
    await db.commit()
    await db.refresh(new_workout)

    return CreateWorkoutResponseSchema(
        workout=WorkoutSchema(
            id=new_workout.id,
            name=new_workout.name,
            description=new_workout.description,
            total_time=new_workout.total_time,
            rest_time=new_workout.rest_time,
            user_id=new_workout.user_id,
            exercise_id=new_workout.exercise_id,
            efficiency=new_workout.efficiency,
            created_at=new_workout.created_at,
        ),
        message="Workout created successfully"
    )


@router.post(
    "/sessions",
    response_description="Add a new workout session to a workout",
    responses={
        200: {"model": CreateWorkoutSessionResponseSchema, "description": "Workout session added successfully"},
        401: {"model": ErrorResponseSchema,
              "description": "Токен недействителен, срок действия истек или не предоставлен"},
        404: {"model": ErrorResponseSchema, "description": "User or workout not found"},
    }
)
async def add_new_workout_session(
    data: CreateWorkoutSessionSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(jwt_verify)
):
    # noinspection PyTypeChecker
    query = select(Workout).where(Workout.id == data.workout_id)
    result = await db.execute(query)
    workout = result.scalars().first()

    if not workout:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({
                "detail": "Workout not found"
            })
        )

    new_workout_session = WorkoutSession(
        user_id=user.id,
        workout_id=data.workout_id,
        end_time=data.end_time,
        repetitions=data.repetitions
    )

    db.add(new_workout_session)
    await db.commit()
    await db.refresh(new_workout_session)

    return CreateWorkoutSessionResponseSchema(
        session=WorkoutSessionSchema(
            id=new_workout_session.id,
            user_id=new_workout_session.user_id,
            workout_id=new_workout_session.workout_id,
            end_time=new_workout_session.end_time,
            repetitions=new_workout_session.repetitions,
            start_time=new_workout_session.start_time
        ),
        message="Workout session added successfully."
    )
