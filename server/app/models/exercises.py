from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
)
from app.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    total_time = Column(Integer, nullable=False)
    rest_time = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
