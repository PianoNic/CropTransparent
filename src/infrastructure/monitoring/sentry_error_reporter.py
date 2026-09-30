import logging
from typing import Any

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

logger = logging.getLogger(__name__)

_SERVER_ERRORS = set(range(500, 600))
_SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key", "x-auth-token"}
_FILTERED = "[Filtered]"


class SentryErrorReporter:
    def __init__(
        self, dsn: str | None, environment: str, release: str, traces_sample_rate: float = 0.1
    ) -> None:
        self._dsn = dsn
        self._environment = environment
        self._release = release
        self._traces_sample_rate = traces_sample_rate

    def initialize(self) -> bool:
        if not self._dsn:
            logger.info("SENTRY_DSN is not set, error reporting is disabled")
            return False

        sentry_sdk.init(
            dsn=self._dsn,
            environment=self._environment,
            release=self._release,
            traces_sample_rate=self._traces_sample_rate,
            send_default_pii=False,
            attach_stacktrace=True,
            integrations=[
                StarletteIntegration(
                    transaction_style="endpoint", failed_request_status_codes=_SERVER_ERRORS
                ),
                FastApiIntegration(transaction_style="endpoint", failed_request_status_codes=_SERVER_ERRORS),
                LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            ],
            before_send=self.scrub,
        )
        logger.info("Sentry error reporting enabled for %s %s", self._environment, self._release)
        return True

    @staticmethod
    def scrub(event: dict[str, Any], _hint: dict[str, Any]) -> dict[str, Any]:
        request = event.get("request") or {}
        if "cookies" in request:
            request["cookies"] = _FILTERED
        headers = request.get("headers") or {}
        for name in list(headers):
            if name.lower() in _SENSITIVE_HEADERS:
                headers[name] = _FILTERED
        return event
