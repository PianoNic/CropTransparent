import os
from pathlib import Path

# the release workflow writes the tag's version here; environment variables still win
_PROPERTIES_FILE = Path(__file__).resolve().parents[3] / "application.properties"


def _read_properties() -> dict[str, str]:
    if not _PROPERTIES_FILE.is_file():
        return {}
    lines = _PROPERTIES_FILE.read_text(encoding="utf-8").splitlines()
    return dict(line.split("=", 1) for line in lines if "=" in line and not line.startswith("#"))


class EnvironmentApplicationInfoProvider:
    ENVIRONMENT_VARIABLE = "APP_ENVIRONMENT"
    VERSION_VARIABLE = "APP_VERSION"
    UNKNOWN_ENVIRONMENT = "unknown environment"
    UNKNOWN_VERSION = "unknown version"

    def __init__(self) -> None:
        self._properties = _read_properties()

    def _get(self, key: str, default: str) -> str:
        return os.environ.get(key) or self._properties.get(key, default).strip()

    def get_environment(self) -> str:
        return self._get(self.ENVIRONMENT_VARIABLE, self.UNKNOWN_ENVIRONMENT)

    def get_version(self) -> str:
        return self._get(self.VERSION_VARIABLE, self.UNKNOWN_VERSION)
