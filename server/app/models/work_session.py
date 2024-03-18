from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.core.database import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    repetitions = Column(Integer, nullable=True, default=0)
    start_time = Column(DateTime(timezone=True), default=func.now())
