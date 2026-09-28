from src.application.abstractions.raster_image_cropper import IRasterImageCropper
from src.application.abstractions.vector_image_cropper import IVectorImageCropper
from src.application.commands.crop_image.crop_image_command import CropImageCommand
from src.domain.exceptions import EmptyUploadError, ImageTooLargeError
from src.domain.models.cropped_image import CroppedImage

MAX_UPLOAD_BYTES = 25 * 1024 * 1024

_SVG_EXTENSION = ".svg"
_SVG_MEDIA_TYPE = "image/svg+xml"


class CropImageCommandHandler:
    def __init__(
        self,
        raster_cropper: IRasterImageCropper,
        vector_cropper: IVectorImageCropper,
    ) -> None:
        self._raster_cropper = raster_cropper
        self._vector_cropper = vector_cropper

    async def handle(self, command: CropImageCommand) -> CroppedImage:
        self._ensure_upload_is_acceptable(command)

        if self._is_vector(command):
            return self._vector_cropper.crop(command.content)
        return self._raster_cropper.crop(command.content)

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
