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

@router.get("/", response_class=HTMLResponse)
async def view_characters(request: Request, db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    character_count = db.query(Character).count()
    return templates.TemplateResponse("view_characters.html", {
        "request": request,
        "characters": characters,
        "character_count": character_count
    })
