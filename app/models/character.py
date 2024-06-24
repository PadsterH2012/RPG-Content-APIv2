from sqlalchemy import Column, Integer, String
from app.database import Base

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sex = Column(String, index=True)
    age = Column(String, index=True)
    traits = Column(String, index=True)
    behaviors = Column(String, index=True)
    background = Column(String, index=True)
