from dataclasses import dataclass
from typing import Union, List


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