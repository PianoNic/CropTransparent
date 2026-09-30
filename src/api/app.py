import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.types import Scope

from src.api.router_registry import router_registry
from src.infrastructure.configuration.environment_application_info_provider import (
    EnvironmentApplicationInfoProvider,
)
from src.infrastructure.dependency_injection import build_mediator
from src.infrastructure.monitoring.sentry_error_reporter import SentryErrorReporter

logging.basicConfig(level=logging.INFO)
load_dotenv()


class SpaStaticFiles(StaticFiles):
    # Any path that is not a built file gets index.html, so client-side routes survive a reload.
    # Unknown /api paths still 404, otherwise a typo in an API call would come back as HTML.
    async def get_response(self, path: str, scope: Scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as error:
            if error.status_code != 404 or path.split("/", 1)[0] == "api":
                raise
            return await super().get_response("index.html", scope)


def create_app() -> FastAPI:
    info = EnvironmentApplicationInfoProvider()
    SentryErrorReporter(os.getenv("SENTRY_DSN"), info.get_environment(), info.get_version()).initialize()

    application = FastAPI(
        title="Smart Image Cropper API",
        description="API for automatically cropping transparent areas and backgrounds",
        version="1.0.0",
    )

    application.state.mediator = build_mediator()
    router_registry.auto_register(application)

    # mounted last so /api and /docs routes take precedence
    frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if frontend_dist.is_dir():
        application.mount("/", SpaStaticFiles(directory=frontend_dist, html=True), name="frontend")
    return application


app = create_app()
