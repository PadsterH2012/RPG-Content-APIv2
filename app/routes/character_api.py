from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.character import Character as CharacterModel
from pydantic import BaseModel
import random

router = APIRouter()

class Character(BaseModel):
    id: int
    name: str
    sex: str
    age: str
    traits: str
    behaviors: str
    background: str
    book_title: str
    author: str
    dialogue_examples: str
    genre: str

    class Config:
        orm_mode = True

@router.get("/characters/", response_model=List[Character])
async def get_characters(db: Session = Depends(get_db)):
    characters = db.query(CharacterModel).all()
    return characters

@router.get("/characters/random", response_model=Character)
async def get_random_character(db: Session = Depends(get_db)):
    characters = db.query(CharacterModel).all()
    if not characters:
        raise HTTPException(status_code=404, detail="No characters found")
    return random.choice(characters)
