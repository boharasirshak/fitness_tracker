from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
)

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=True, default="")
    hashed_password: str = Column(String, nullable=False)
    gender = Column(String, nullable=True, default="")
    height = Column(Integer, nullable=True, default=0)
    weight = Column(Integer, nullable=True, default=0)
    activity_level = Column(Integer, nullable=True, default=0)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
