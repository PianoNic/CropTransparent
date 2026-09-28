from typing import Protocol, runtime_checkable

from src.domain.models.cropped_image import CroppedImage


@runtime_checkable
class IVectorImageCropper(Protocol):
    def crop(self, content: bytes) -> CroppedImage: ...
