from fastapi import APIRouter

router = APIRouter(
    prefix="/exercises"
)

exercises_data = [
    {"Timer": 60, "Exercises": "High Knees", "Repetitions": 15},
    {"Timer": 60, "Exercises": "Jumping Jacks", "Repetitions": 15},
]

@router.get("/getexer")
async def get_exercises():
    pass

@router.get("/all_exercises")
async def get_all_exercises():
    return exercises_data

@router.put("/all_exercises/{index}")
async def edit_exercise():
    pass
