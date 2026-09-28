from fastapi import APIRouter

from src.api.dependencies import MediatorDependency
from src.application.queries.get_application_info.application_info import ApplicationInfo
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)

router = APIRouter(prefix="/api", tags=["App Info"])


@router.get("/app-info")
async def get_application_info(mediator: MediatorDependency) -> dict[str, str]:
    result: ApplicationInfo = await mediator.send(GetApplicationInfoQuery())
    return {"environment": result.environment, "version": result.version}
