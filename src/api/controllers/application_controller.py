from fastapi import APIRouter, Depends
from mediatorx import Mediator

from src.api.controller import controller
from src.api.dependencies import get_mediator
from src.application.queries.get_application_info.application_info import ApplicationInfo
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)

router = APIRouter(prefix="/api", tags=["App Info"])


@controller(router)
class ApplicationController:
    mediator: Mediator = Depends(get_mediator)

    @router.get("/app-info")
    async def get_application_info(self) -> dict[str, str]:
        result: ApplicationInfo = await self.mediator.send(GetApplicationInfoQuery())
        return {"environment": result.environment, "version": result.version}
