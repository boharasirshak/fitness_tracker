from datetime import datetime

from pydantic import BaseModel

from app.schemas.exercises import ExerciseSchema


class WorkoutSessionSchema(BaseModel):
    id: int
    user_id: int
    workout_id: int
    start_time: datetime
    end_time: datetime
    repetitions: int


class DetailedWorkoutSchema(BaseModel):
    id: int
    name: str
    description: str
    total_time: int
    rest_time: int
    user_id: int
    exercise_id: int
    efficiency: int
    created_at: datetime

    exercise: ExerciseSchema
    sessions: list[WorkoutSessionSchema]


class WorkoutSchema(BaseModel):
    id: int
    name: str
    description: str
    total_time: int
    rest_time: int
    efficiency: int
    user_id: int
    exercise_id: int
    created_at: datetime


class AllWorkoutsSchema(BaseModel):
    workouts: list[DetailedWorkoutSchema]


class CreateWorkoutSchema(BaseModel):
    name: str
    description: str
    total_time: int
    rest_time: int
    exercise_id: int


class CreateWorkoutSessionSchema(BaseModel):
    workout_id: int
    start_time: datetime
    end_time: datetime
    repetitions: int


class CreateWorkoutResponseSchema(BaseModel):
    workout: WorkoutSchema
    message: str


class CreateWorkoutSessionResponseSchema(BaseModel):
    session: WorkoutSessionSchema
    message: str
