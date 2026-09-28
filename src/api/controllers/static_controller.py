from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from mediatorx import Mediator

from src.api.dependencies import MediatorDependency
from src.application.queries.get_application_info.application_info import ApplicationInfo
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, mediator: MediatorDependency) -> HTMLResponse:
    return await _render(request, mediator, "index.html")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, mediator: MediatorDependency) -> HTMLResponse:
    return await _render(request, mediator, "about.html")


async def _render(request: Request, mediator: Mediator, template_name: str) -> HTMLResponse:
    info: ApplicationInfo = await mediator.send(GetApplicationInfoQuery())
    release_url = f"https://github.com/Pianonic/CropTransparent/releases/tag/{info.version}"

    return request.app.state.templates.TemplateResponse(
        request,
        template_name,
        {
            "environment": info.environment,
            "version": info.version,
            "version_url": release_url,
        },
    )
