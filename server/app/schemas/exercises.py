from datetime import datetime

from pydantic import BaseModel


class ExerciseSchema(BaseModel):
    id: int
    name: str
    description: str
    video_link: str
    description: str
    created_at: datetime


class AllExercisesResponse(BaseModel):
    exercises: list[ExerciseSchema]
