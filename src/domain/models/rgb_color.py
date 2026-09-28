from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RgbColor:
    red: int
    green: int
    blue: int

    def as_tuple(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue
