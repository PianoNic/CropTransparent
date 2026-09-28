from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApplicationInfo:
    environment: str
    version: str
