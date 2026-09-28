from dataclasses import dataclass

from mediatorx import ICommand

from src.domain.models.cropped_image import CroppedImage


@dataclass(frozen=True, slots=True)
class CropImageCommand(ICommand[CroppedImage]):
    content: bytes
    file_name: str
    content_type: str | None = None
