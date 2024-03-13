from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
)

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, default="")
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return (f"User(id={self.id}, email={self.email}, username={self.username}, role_id={self.role_id}, "
                f"is_active={self.is_active}, is_superuser={self.is_superuser}, is_verified={self.is_verified})")
