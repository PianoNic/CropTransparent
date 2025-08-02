import os
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    templates = request.app.state.templates
    environment = os.environ.get('FLASK_ENV', 'unknown')
    version = os.environ.get('APP_VERSION', 'unknown')
    version_url = f"https://github.com/Pianonic/CropTransparent/releases/tag/{version}"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "environment": environment,
        "version": version,
        "version_url": version_url
    })

@router.get("/about", response_class=HTMLResponse, include_in_schema=False)
def about(request: Request):
    templates = request.app.state.templates
    environment = os.environ.get('FLASK_ENV', 'unknown')
    version = os.environ.get('APP_VERSION', 'unknown')
    version_url = f"https://github.com/Pianonic/CropTransparent/releases/tag/{version}"
    return templates.TemplateResponse("about.html", {
        "request": request,
        "environment": environment,
        "version": version,
        "version_url": version_url
    })