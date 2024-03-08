from sqlalchemy import Column, Integer, String, MetaData
from src.database import Base

metadata = MetaData()


class Operation(Base):
    __tablename__ = "operations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String)
    birthday = (Column(String, nullable=False),)
    gender = Column(String)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    acticity = Column(String, nullable=False)

    def __repr__(self):
        return f"Operation(id={self.id}, Name={self.name}, Surname={self.surname}, Birthday = {self.birthday}, Gender = {self.gender} Height = {self.height}, Weight = {self.weight}, Activity = {self.acticity})"
