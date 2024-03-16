import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
)

from app.core.database import Base


class ActivityLevel(enum.Enum):
    NOT_GIVEN = 0  # Value not given during registration
    BEGINNER = 1  # Doesn't practice much
    AVERAGE = 2  # Practice sports 1-3 timer per week
    ATHLETE = 3  # Practice sports 3-5 times per week
    # add more activity levels here


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=True, default="")
    hashed_password: str = Column(String, nullable=False)
    gender = Column(String, nullable=True, default="")
    height = Column(Integer, nullable=True, default=0)
    weight = Column(Integer, nullable=True, default=0)
    activity_level = Column(Integer, nullable=True, default=ActivityLevel.NOT_GIVEN.value)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
