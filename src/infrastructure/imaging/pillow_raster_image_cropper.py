import io

import numpy as np
from PIL import Image

from src.domain.enums.crop_method import CropMethod
from src.domain.enums.image_format import ImageFormat
from src.domain.exceptions import InvalidImageError
from src.domain.models.cropped_image import CroppedImage
from src.domain.models.image_size import ImageSize
from src.domain.models.rgb_color import RgbColor

_JPEG_QUALITY = 95
_DEFAULT_BACKGROUND_THRESHOLD = 30
_DEFAULT_CORNER_OFFSET = 5
_SUPPORTED_PILLOW_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}


class PillowRasterImageCropper:
    def __init__(
        self,
        background_threshold: float = _DEFAULT_BACKGROUND_THRESHOLD,
        corner_offset: int = _DEFAULT_CORNER_OFFSET,
    ) -> None:
        self._background_threshold = background_threshold
        self._corner_offset = corner_offset

    def crop(self, content: bytes) -> CroppedImage:
        try:
            image = Image.open(io.BytesIO(content))
            image.load()
        except Exception as error:
            raise InvalidImageError("The uploaded file is not a readable image") from error

        if self._has_transparency(image):
            return self._crop_transparent(image)
        return self._crop_background_colour(image)

    @staticmethod
    def _has_transparency(image: Image.Image) -> bool:
        if image.mode not in ("RGBA", "LA") and "transparency" not in image.info:
            return False
        alpha = np.array(image.convert("RGBA").getchannel("A"))
        return bool(alpha.min() < 255)

    def _crop_transparent(self, image: Image.Image) -> CroppedImage:
        rgba_image = image.convert("RGBA")
        bounds = rgba_image.getbbox()
        cropped = rgba_image.crop(bounds) if bounds else rgba_image

        return CroppedImage(
            content=self._encode(cropped, ImageFormat.PNG),
            original_size=ImageSize(*rgba_image.size),
            cropped_size=ImageSize(*cropped.size),
            crop_method=CropMethod.TRANSPARENT,
            output_format=ImageFormat.PNG,
        )

    def _crop_background_colour(self, image: Image.Image) -> CroppedImage:
        output_format = self._resolve_output_format(image)
        working_image = image if image.mode in ("RGB", "RGBA") else image.convert("RGB")

        background = self._sample_background_colour(working_image)
        bounds = self._find_foreground_bounds(working_image, background)
        cropped = working_image.crop(bounds) if bounds else working_image

        return CroppedImage(
            content=self._encode(cropped, output_format),
            original_size=ImageSize(*working_image.size),
            cropped_size=ImageSize(*cropped.size),
            crop_method=CropMethod.COLOR_BACKGROUND,
            output_format=output_format,
            background_color=background,
        )

    def _sample_background_colour(self, image: Image.Image) -> RgbColor:
        width, height = image.size
        offset = min(self._corner_offset, width // 4, height // 4)
        corners = (
            (offset, offset),
            (width - offset - 1, offset),
            (offset, height - offset - 1),
            (width - offset - 1, height - offset - 1),
        )

        samples = [image.getpixel(corner)[:3] for corner in corners]
        channels = zip(*samples, strict=True)
        return RgbColor(*(sum(channel) // len(samples) for channel in channels))

    def _find_foreground_bounds(
        self,
        image: Image.Image,
        background: RgbColor,
    ) -> tuple[int, int, int, int] | None:
        pixels = np.array(image)[:, :, :3].astype(np.float32)
        distances = np.sqrt(np.sum((pixels - np.array(background.as_tuple())) ** 2, axis=2))
        rows, columns = np.where(distances > self._background_threshold)
        if rows.size == 0:
            return None
        return int(columns.min()), int(rows.min()), int(columns.max()) + 1, int(rows.max()) + 1

    @staticmethod
    def _resolve_output_format(image: Image.Image) -> ImageFormat:
        if image.format in _SUPPORTED_PILLOW_FORMATS:
            return ImageFormat(image.format.lower())
        return ImageFormat.PNG

    @staticmethod
    def _encode(image: Image.Image, output_format: ImageFormat) -> bytes:
        if output_format is ImageFormat.JPEG and image.mode in ("RGBA", "LA"):
            opaque = Image.new("RGB", image.size, (255, 255, 255))
            opaque.paste(image, mask=image.convert("RGBA").getchannel("A"))
            image = opaque

        buffer = io.BytesIO()
        options: dict[str, object] = {"format": output_format.name}
        if output_format is ImageFormat.JPEG:
            options |= {"quality": _JPEG_QUALITY, "optimize": True}

        image.save(buffer, **options)
        return buffer.getvalue()
