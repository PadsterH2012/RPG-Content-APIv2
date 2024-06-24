from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database import get_db
from app.models.character import Character
from app.ollama_client import generate_content
import logging

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger('app')

@router.get("/character_chat/{character_id}")
async def character_chat(character_id: int, request: Request, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return templates.TemplateResponse("character_chat.html", {"request": request, "character": character})

@router.post("/chat")
async def chat(message: dict, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == message["character_id"]).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    system_prompt = f"You are chatting with {character.name}. Here are the details: \n" \
                    f"Sex: {character.sex}\nAge: {character.age}\nTraits: {character.traits}\n" \
                    f"Behaviors: {character.behaviors}\nBackground: {character.background}\n" \
                    f"Book Title: {character.book_title}\nAuthor: {character.author}\n" \
                    f"Dialogue Examples: {character.dialogue_examples}\nGenre: {character.genre}"
    
    user_message = message["message"]
    prompt = f"{system_prompt}\n\nUser: {user_message}\n{character.name}:"
    
    response = generate_content(prompt)
    return {"response": response.strip()}
