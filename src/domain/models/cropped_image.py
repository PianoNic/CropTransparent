from dataclasses import dataclass

from src.domain.enums.crop_method import CropMethod
from src.domain.enums.image_format import ImageFormat
from src.domain.models.image_size import ImageSize
from src.domain.models.rgb_color import RgbColor


@dataclass(frozen=True, slots=True)
class CroppedImage:
    content: bytes
    original_size: ImageSize
    cropped_size: ImageSize
    crop_method: CropMethod
    output_format: ImageFormat
    background_color: RgbColor | None = None

    @property
    def saved_percentage(self) -> int:
        if self.original_size.area == 0:
            return 0
        ratio = 1 - (self.cropped_size.area / self.original_size.area)
        return round(ratio * 100)
