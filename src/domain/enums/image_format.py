from enum import StrEnum


class ImageFormat(StrEnum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    GIF = "gif"
    SVG = "svg"

    @property
    def file_extension(self) -> str:
        return "jpg" if self is ImageFormat.JPEG else self.value

    @property
    def media_type(self) -> str:
        return "image/svg+xml" if self is ImageFormat.SVG else f"image/{self.value}"

    @classmethod
    def from_extension(cls, extension: str) -> "ImageFormat | None":
        normalised = extension.lower().lstrip(".")
        if normalised == "jpg":
            return cls.JPEG
        try:
            return cls(normalised)
        except ValueError:
            return None
