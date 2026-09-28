import importlib
import logging
from pathlib import Path

import colorlog
from fastapi import APIRouter, FastAPI

_handler = colorlog.StreamHandler()
_handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)sINFO%(reset)s:     %(message)s",
        log_colors={
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)

logger = colorlog.getLogger(__name__)
logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False


class RouterRegistry:
    def __init__(self, controllers_package: str = "src.api.controllers") -> None:
        self._controllers_package = controllers_package
        self.registered_count = 0

    def auto_register(self, app: FastAPI, controllers_dir: Path | None = None) -> int:
        if controllers_dir is None:
            controllers_dir = Path(__file__).resolve().parent / "controllers"

        if not controllers_dir.exists():
            logger.warning(f"Controllers directory not found: {controllers_dir}")
            return 0

        self.registered_count = 0
        for file_path in sorted(controllers_dir.glob("*.py")):
            if file_path.name.startswith(("__", ".")):
                continue
            if self._register_module(app, file_path.stem):
                self.registered_count += 1

        logger.info(f"Successfully registered {self.registered_count} controller(s)")
        return self.registered_count

    def _register_module(self, app: FastAPI, module_stem: str) -> bool:
        module_name = f"{self._controllers_package}.{module_stem}"
        try:
            module = importlib.import_module(module_name)
        except ImportError as error:
            logger.error(f"Import failed: {module_name} - {error}")
            return False

        router = getattr(module, "router", None)
        if not isinstance(router, APIRouter):
            logger.debug(f"No router found in: {module_name}")
            return False

        app.include_router(router)
        logger.info(f"Registered: {module_stem}")
        return True


router_registry = RouterRegistry()
