import os


class EnvironmentApplicationInfoProvider:
    ENVIRONMENT_VARIABLE = "FLASK_ENV"
    VERSION_VARIABLE = "APP_VERSION"
    UNKNOWN_ENVIRONMENT = "unknown environment"
    UNKNOWN_VERSION = "unknown version"

    def get_environment(self) -> str:
        return os.environ.get(self.ENVIRONMENT_VARIABLE, self.UNKNOWN_ENVIRONMENT)

    def get_version(self) -> str:
        return os.environ.get(self.VERSION_VARIABLE, self.UNKNOWN_VERSION)
