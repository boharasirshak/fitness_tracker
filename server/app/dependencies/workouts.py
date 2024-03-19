from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Depends, Request

from app.models.workouts import Workout
from app.core.database import get_db

async def workout_verify( 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    workout_id = request.path_params.get("workout_id")
    if id is None:
        raise HTTPException(status_code=404, detail="Workout not passed in the path")
      
    try:
        workout_id = int(workout_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token: user_id is not an integer")

    # noinspection PyTypeChecker
    query = select(Workout).where(Workout.id == workout_id)
    result = await db.execute(query)
    workout = result.scalar()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
      
    return workout
