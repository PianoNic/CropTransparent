from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ImageSize:
    width: int
    height: int

    @property
    def area(self) -> int:
        return self.width * self.height

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
