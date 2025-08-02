from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.api.router_registry import router_registry
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(
    title="Smart Image Cropper API",
    description="API for automatically cropping transparent areas and backgrounds from images",
    version="1.0.0"
)

base_dir = Path(__file__).parent.parent

# Mount static files and templates using pathlib for cleaner paths
static_dir = base_dir / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates_dir = base_dir / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))
app.state.templates = templates

# Auto-register all controllers
router_registry.auto_register(app)