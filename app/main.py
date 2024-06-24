import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes import character, quest, trait, character_behavior, pdf_upload, view_characters
from app.database import create_tables
from app.config import settings
import os

# Set up logging
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log_file = "app.log"

file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*10, backupCount=3)
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.DEBUG,
                    handlers=[file_handler, console_handler])

logger = logging.getLogger(__name__)

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
app.include_router(view_characters.router, tags=["view_characters"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
