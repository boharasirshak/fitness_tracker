from app.core.database import Base
from sqlalchemy import Column, Integer, String


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise = Column(String, nullable=False)
    timer = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Exercise(exercise={self.exercise}, timer={self.timer}, repetitions={self.repetitions})"
