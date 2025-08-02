from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.api.router_registry import router_registry
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(
    title="Smart Image Cropper API",
    description="API for automatically cropping transparent areas and backgrounds from images",
    version="1.0.0"
)

# Mount static files and templates
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "templates")
templates = Jinja2Templates(directory=templates_dir)
app.state.templates = templates

# Auto-register all controllers
router_registry.auto_register(app)