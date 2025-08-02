from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.controllers.image_controller import register_routes
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create and configure the app
app = FastAPI(
    title="Smart Image Cropper API",
    description="API for automatically cropping transparent areas and backgrounds from images",
    version="1.0.0"
)

# Mount static files with absolute path
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configure templates with absolute path
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Make templates available to controllers
app.state.templates = templates

# Register routes
register_routes(app)