from dataclasses import dataclass

from mediatorx import IQuery

from src.application.queries.get_application_info.application_info import ApplicationInfo


@dataclass(frozen=True, slots=True)
class GetApplicationInfoQuery(IQuery[ApplicationInfo]):
    pass
