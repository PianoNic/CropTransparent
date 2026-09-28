from src.application.abstractions.application_info_provider import IApplicationInfoProvider
from src.application.queries.get_application_info.application_info import ApplicationInfo
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)


class GetApplicationInfoQueryHandler:
    def __init__(self, info_provider: IApplicationInfoProvider) -> None:
        self._info_provider = info_provider

    async def handle(self, _query: GetApplicationInfoQuery) -> ApplicationInfo:
        return ApplicationInfo(
            environment=self._info_provider.get_environment(),
            version=self._info_provider.get_version(),
        )
