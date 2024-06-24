from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.character import Character
from app.config import settings
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(settings.BASE_DIR, "templates"))

@router.get("/view_characters", response_class=HTMLResponse)
async def view_characters(request: Request, db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    return templates.TemplateResponse("view_characters.html", {
        "request": request,
        "characters": characters
    })

@router.get("/character/{character_id}", response_class=HTMLResponse)
async def view_character(request: Request, character_id: int, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        return HTMLResponse(content="Character not found", status_code=404)
    return templates.TemplateResponse("view_character.html", {
        "request": request,
        "character": character
    })
