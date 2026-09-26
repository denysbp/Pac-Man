from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Any, Callable
from ..loader.loader import ConfigLoader


@dataclass
class ConfigData:
    """Data class used for store configs"""
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
    """Store config for each level"""
    width: int
    height: int


class Rect:
    """
    Responsible for representing a rectangular area

    ```
    Attributes
    __________
    x: int
        represent the horizontal position of the rectangle
    y: int
        represent the vertical position of the rectangle
    width: int
        represent the width of the rectangle
    height: int
        represent the height of the rectangle

    Methods
    _______
    left:
        return the left coordinate of the rectangle
    right:
        return the right coordinate of the rectangle
    top:
        return the top coordinate of the rectangle
    bottom:
        return the bottom coordinate of the rectangle
    colliderect():
        verify if this rectangle overlaps another rectangle
    """

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
        """Return the left coordinate of the rectangle"""
        return self.x

    @property
    def right(self) -> int:
        """Return the right coordinate of the rectangle"""
        return self.x + self.width

    @property
    def top(self) -> int:
        """Return the top coordinate of the rectangle"""
        return self.y

    @property
    def bottom(self) -> int:
        """Return the botton coordinate of the rectangle"""
        return self.y + self.height

    def colliderect(self, other: Rect) -> bool:
        """verify if this rectangle overlaps another rectangle"""
        return (
            self.left < other.right and
            self.right > other.left and
            self.top < other.bottom and
            self.bottom > other.top
        )


class Memory:
    """
    Responsible for storing image memory information

    Attributes
    __________
    data: Any
        store the image memory buffer
    bpp: int
        represent the number of bits used by each pixel
    size_line: int
        represent the number of bytes occupied by one image row
    endian: int
        represent the byte order used by the image

    Methods
    _______
    save():
        call the provided function and store the returned image
        memory information
    """
    def __init__(self) -> None:
        self.data: Any
        self.bpp: int
        self.size_line: int
        self.endian: int

    def save(self, function: Callable, arg: Any | None) -> None:
        self.data, self.bpp, self.size_line, self.endian = function(arg)


def alocate_levels(data: ConfigLoader) -> list[Level]:
    """
    Allocate the levels defined in the configuration

    Args:
        data: ConfigLoader
            store the configuration values used to create the levels

    Returns:
        list[Level]
            list containing all allocated level objects
    """
    all_data = []
    for level in data.configs["level"]:
        width, height = level.values()
        obj = Level(
            width,
            height
        )
        all_data.append(obj)
    return all_data


def create_config(data: ConfigLoader) -> ConfigData:
    """
    Create the game configuration from the loaded values

    Args:
        data: ConfigLoader
            store the loaded configuration values

    Returns:
        ConfigData
            configuration object containing the game settings
    """
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
