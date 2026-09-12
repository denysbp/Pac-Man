from mlx import Mlx
from typing import Any, Union


class Bot:
    def __init__(
        self,
        *
        img: Union[Any | None],
        img_width: int,
        img_height: int,
        x: int,
        y: int,
    ):
        self.img = img
        self.height = img_height
        self.width = img_width
        self.x = x
        self.y = y