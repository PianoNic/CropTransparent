import io

import numpy as np
from PIL import Image, ImageSequence

from src.domain.enums.crop_method import CropMethod
from src.domain.enums.image_format import ImageFormat
from src.domain.exceptions import ImageTooLargeError, InvalidImageError
from src.domain.models.cropped_image import CroppedImage
from src.domain.models.image_size import ImageSize
from src.domain.models.rgb_color import RgbColor

_JPEG_QUALITY = 95
_DEFAULT_BACKGROUND_THRESHOLD = 30
_DEFAULT_CORNER_OFFSET = 5
_SUPPORTED_PILLOW_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}
_MAX_PIXELS = 50_000_000
_MAX_ANIMATION_PIXELS = 200_000_000


class PillowRasterImageCropper:
    def __init__(
        self,
        background_threshold: float = _DEFAULT_BACKGROUND_THRESHOLD,
        corner_offset: int = _DEFAULT_CORNER_OFFSET,
        max_pixels: int = _MAX_PIXELS,
        max_animation_pixels: int = _MAX_ANIMATION_PIXELS,
    ) -> None:
        self._background_threshold = background_threshold
        self._corner_offset = corner_offset
        self._max_pixels = max_pixels
        self._max_animation_pixels = max_animation_pixels

    def crop(self, content: bytes) -> CroppedImage:
        try:
            image = Image.open(io.BytesIO(content))
        except Image.DecompressionBombError as error:
            raise ImageTooLargeError("Image dimensions are too large") from error
        except Exception as error:
            raise InvalidImageError("The uploaded file is not a readable image") from error

        # open() only reads the header, so this runs before any pixel data is decoded
        self._ensure_within_pixel_limits(image)
        try:
            image.load()
        except Exception as error:
            raise InvalidImageError("The uploaded file is not a readable image") from error

        if getattr(image, "n_frames", 1) > 1:
            return self._crop_animated(image)
        if self._has_transparency(image):
            return self._crop_transparent(image)
        return self._crop_background_colour(image)

    def _ensure_within_pixel_limits(self, image: Image.Image) -> None:
        width, height = image.size
        if width * height > self._max_pixels:
            limit = self._max_pixels // 1_000_000
            raise ImageTooLargeError(f"Image too large ({width} × {height}, max {limit} megapixels)")
        frames = getattr(image, "n_frames", 1)
        if frames > 1 and frames * width * height > self._max_animation_pixels:
            raise ImageTooLargeError(f"Animation too large ({frames} frames of {width} × {height})")

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

    def _crop_animated(self, image: Image.Image) -> CroppedImage:
        # one box for every frame (union of each frame's content) so the animation stays aligned
        frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(image)]
        durations = [frame.info.get("duration", 100) for frame in ImageSequence.Iterator(image)]
        transparent = any(self._has_transparency(frame) for frame in frames)

        background = None if transparent else self._sample_background_colour(frames[0])
        boxes = [
            frame.getbbox(alpha_only=True) if transparent else self._find_foreground_bounds(frame, background)
            for frame in frames
        ]
        boxes = [box for box in boxes if box]
        bounds = (
            (
                min(b[0] for b in boxes),
                min(b[1] for b in boxes),
                max(b[2] for b in boxes),
                max(b[3] for b in boxes),
            )
            if boxes
            else (0, 0, *image.size)
        )
        cropped = [frame.crop(bounds) for frame in frames]

        output_format = self._resolve_output_format(image)
        buffer = io.BytesIO()
        cropped[0].save(
            buffer,
            format=output_format.name,
            save_all=True,
            append_images=cropped[1:],
            duration=durations,
            loop=image.info.get("loop", 0),
            disposal=2,
        )

        return CroppedImage(
            content=buffer.getvalue(),
            original_size=ImageSize(*image.size),
            cropped_size=ImageSize(*cropped[0].size),
            crop_method=CropMethod.TRANSPARENT if transparent else CropMethod.COLOR_BACKGROUND,
            output_format=output_format,
            background_color=background,
        )

    def _crop_background_colour(self, image: Image.Image) -> CroppedImage:
        output_format = self._resolve_output_format(image)
        working_image = image if image.mode in ("RGB", "RGBA") else image.convert("RGB")

        background = self._sample_background_colour(working_image)
        bounds = self._find_foreground_bounds(working_image, background, lossy=image.format == "JPEG")
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
        lossy: bool = False,
    ) -> tuple[int, int, int, int] | None:
        pixels = np.array(image)[:, :, :3].astype(np.float32)
        distances = np.sqrt(np.sum((pixels - np.array(background.as_tuple())) ** 2, axis=2))
        rows, columns = np.where(distances > self._background_threshold)
        if rows.size == 0:
            return None
        bounds = int(columns.min()), int(rows.min()), int(columns.max()) + 1, int(rows.max()) + 1
        return self._trim_compression_halo(distances, bounds) if lossy else bounds

    @staticmethod
    def _trim_compression_halo(
        distances: np.ndarray,
        bounds: tuple[int, int, int, int],
    ) -> tuple[int, int, int, int]:
        # JPEG ringing / chroma bleed leaves a faint fringe (up to one 8px block) outside real edges.
        # Peel an outer line while it is less than half as strong as the strongest line within the next block.
        left, top, right, bottom = bounds
        while right - left > 9:
            if distances[top:bottom, left].max() < 0.5 * distances[top:bottom, left + 1 : left + 9].max():
                left += 1
            elif (
                distances[top:bottom, right - 1].max()
                < 0.5 * distances[top:bottom, right - 9 : right - 1].max()
            ):
                right -= 1
            else:
                break
        while bottom - top > 9:
            if distances[top, left:right].max() < 0.5 * distances[top + 1 : top + 9, left:right].max():
                top += 1
            elif (
                distances[bottom - 1, left:right].max()
                < 0.5 * distances[bottom - 9 : bottom - 1, left:right].max()
            ):
                bottom -= 1
            else:
                break
        return left, top, right, bottom

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
