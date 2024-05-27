from datetime import datetime

from pydantic import BaseModel

from app.schemas.exercises import ExerciseSchema


class WorkoutSessionSchema(BaseModel):
    id: int
    repetitions: int


class WorkoutExerciseSchema(BaseModel):
    id: int
    total_time: int
    rest_time: int
    created_at: datetime

    exercise: ExerciseSchema
    sessions: list[WorkoutSessionSchema]


class WorkoutSchema(BaseModel):
    id: int
    name: str
    description: str
    efficiency: int
    created_at: datetime

    exercises: list[WorkoutExerciseSchema]


class AllWorkoutsSchema(BaseModel):
    workouts: list[WorkoutSchema]


class CreateWorkoutExerciseSchema(BaseModel):
    exercise_id: int
    total_time: int
    rest_time: int = 0


class CreateWorkoutSessionSchema(BaseModel):
    user_id: int
    workout_exercise_id: int
    repetitions: int


class CreateWorkoutSchema(BaseModel):
    name: str
    description: str
    total_time: int
    user_id: int
    exercises: list[CreateWorkoutExerciseSchema]


class CreateWorkoutResponseSchema(BaseModel):
    message: str


class CreateWorkoutSessionResponseSchema(BaseModel):
    message: str
