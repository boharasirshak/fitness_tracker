from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    ForeignKey,
)
from app.core.database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, unique=True)

    # These two data will be calculated by the neural network

    repetitions = Column(Integer, nullable=False)  # The number of repetitions the user did
    # sets = Column(Integer, nullable=False) # The sets of the exercise the user did

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
