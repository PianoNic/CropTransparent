import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from src.application.abstractions.raster_image_cropper import IRasterImageCropper
from src.application.abstractions.vector_image_cropper import IVectorImageCropper
from src.application.commands.crop_image.crop_image_command import CropImageCommand
from src.domain.exceptions import EmptyUploadError, ImageTooLargeError, ServerBusyError
from src.domain.models.cropped_image import CroppedImage

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
_MAX_PENDING = 16

_SVG_EXTENSION = ".svg"
_SVG_MEDIA_TYPE = "image/svg+xml"


class CropImageCommandHandler:
    def __init__(
        self,
        raster_cropper: IRasterImageCropper,
        vector_cropper: IVectorImageCropper,
        max_concurrent: int = os.cpu_count() or 2,
        max_pending: int = _MAX_PENDING,
    ) -> None:
        self._raster_cropper = raster_cropper
        self._vector_cropper = vector_cropper
        # Cropping is CPU-bound and synchronous; run it on a bounded pool so it never blocks the
        # event loop, and turn requests away once too many are waiting instead of queueing forever.
        self._pool = ThreadPoolExecutor(max_workers=max_concurrent, thread_name_prefix="crop")
        self._max_pending = max_pending
        self._pending = 0

    async def handle(self, command: CropImageCommand) -> CroppedImage:
        self._ensure_upload_is_acceptable(command)
        if self._pending >= self._max_pending:
            raise ServerBusyError("The server is busy cropping other images, try again in a moment")

        cropper = self._vector_cropper if self._is_vector(command) else self._raster_cropper
        self._pending += 1
        try:
            return await asyncio.get_running_loop().run_in_executor(self._pool, cropper.crop, command.content)
        finally:
            self._pending -= 1

    @staticmethod
    def _ensure_upload_is_acceptable(command: CropImageCommand) -> None:
        if not command.content:
            raise EmptyUploadError("No file content was supplied")
        if len(command.content) > MAX_UPLOAD_BYTES:
            limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
            raise ImageTooLargeError(f"File too large (max {limit_mb} MB)")

    @staticmethod
    def _is_vector(command: CropImageCommand) -> bool:
        return (
            command.file_name.lower().endswith(_SVG_EXTENSION)
            or command.content_type == _SVG_MEDIA_TYPE
        )
