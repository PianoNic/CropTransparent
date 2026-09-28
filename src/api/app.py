import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.router_registry import router_registry
from src.infrastructure.dependency_injection import build_mediator

logging.basicConfig(level=logging.INFO)
load_dotenv()


def create_app() -> FastAPI:
    application = FastAPI(
        title="Smart Image Cropper API",
        description="API for automatically cropping transparent areas and backgrounds",
        version="1.0.0",
    )

    frontend_dir = Path(__file__).parent.parent / "frontend"
    application.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    application.state.templates = Jinja2Templates(directory=str(frontend_dir / "templates"))
    application.state.mediator = build_mediator()

    router_registry.auto_register(application)
    return application


app = create_app()
