from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes import character, quest, trait, character_behavior, pdf_upload, view_characters
from app.database import create_tables
from app.config import settings
import os

app = FastAPI(
    title="RPG Content API",
    description="API for generating and managing RPG content",
    version="1.0.0",
)

# Create tables at startup
create_tables()

# Mount the static files directory
app.mount("/static", StaticFiles(directory=os.path.join(settings.BASE_DIR, "static")), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=os.path.join(settings.BASE_DIR, "templates"))

app.include_router(character.router, prefix="/characters", tags=["characters"])
app.include_router(quest.router, prefix="/quests", tags=["quests"])
app.include_router(trait.router, prefix="/traits", tags=["traits"])
app.include_router(character_behavior.router, prefix="/character_behaviors", tags=["character_behaviors"])
app.include_router(pdf_upload.router, prefix="/pdf", tags=["pdf"])
app.include_router(view_characters.router, prefix="/view_characters", tags=["view_characters"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
