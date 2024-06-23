# app/models/character_behavior.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class CharacterBehavior(Base):
    __tablename__ = "character_behaviors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
