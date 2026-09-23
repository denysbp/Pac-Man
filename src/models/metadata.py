from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Any, Callable
from ..loader.loader import ConfigLoader


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
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    def colliderect(self, other: Rect) -> bool:
        return (
            self.left < other.right and
            self.right > other.left and
            self.top < other.bottom and
            self.bottom > other.top
        )


class Memory:
    def __init__(self) -> None:
        self.data: Any
        self.bpp: int
        self.size_line: int
        self.endian: int

    def save(self, function: Callable, arg: Any | None) -> None:
        self.data, self.bpp, self.size_line, self.endian = function(arg)


def alocate_levels(data: ConfigLoader) -> list[Level]:
    all_data = []
    for level in data.configs["level"]:
        widt, height = level.values()
        obj = Level(
            widt,
            height
        )
        all_data.append(obj)
    return all_data


def create_config(data: ConfigLoader) -> ConfigData:
    return ConfigData(
        data.configs["highscore_filename"],
        data.configs["lives"],
        data.configs["pacgum"],
        data.configs["points_per_pacgum"],
        data.configs["points_per_super_pacgum"],
        data.configs["points_per_ghost"],
        data.configs["level_max_time"],
        data.configs["seed"],
    )
