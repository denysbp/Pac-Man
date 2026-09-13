from dataclasses import dataclass
from typing import Union, Any, Callable


@dataclass
class ConfigData:
    highscore_filename: str
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    level_max_time: int
    seed: Union[int | None]

@dataclass
class Level:
    width: int
    height: int

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    def colliderect(self, other):
        return (
            self.left < other.right and
            self.right > other.left and
            self.top < other.bottom and
            self.bottom > other.top
        )


class Memory:
    def __init__(self):
        self.data: Any
        self.bpp: int
        self.size_line: int
        self.endian: int

    def save(self, function: Callable, arg) -> None:
        self.data, self.bpp, self.size_line, self.endian = function(arg)