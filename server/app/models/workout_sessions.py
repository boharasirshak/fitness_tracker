from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_exercise_id = Column(
        Integer, ForeignKey("workout_exercises.id"), nullable=False
    )
    repetitions = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
