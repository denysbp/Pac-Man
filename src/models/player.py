from typing import Any
from .metadata import Rect
class Player:
    def __init__(
        self,
        *,
        span_x: int,
        span_y: int,
        image: Any,
        width: int,
        height: int
    ):
        self.img: Any = image
        self.img_width: int = width
        self.img_height: int = height
        self.x: int = span_x
        self.y: int = span_y
        self.moving = False

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.img_width, self.img_height)
