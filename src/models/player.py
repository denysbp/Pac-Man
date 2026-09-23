from typing import Any, Union
from .metadata import Rect
from .configs import (
    RIGHT, LEFT, TOP, DOWN
)
from mlx.mlx import Mlx


class Player:
    def __init__(
        self,
        *,
        span_x: int,
        span_y: int,
        image: Any,
        width: int,
        height: int,
        mlx_ptr: Any,
        mlx: Mlx,
        lives: int
    ) -> None:
        self._img_name: str = ""
        self._direction: str = "RIGHT"
        self.live: int = lives
        self.img: Any = image
        self.img_width: int = width
        self.img_height: int = height
        self._directions: dict[str, list] = {
            "UP": TOP,
            "LEFT": LEFT,
            "RIGHT": RIGHT,
            "DOWN": DOWN
        }
        self.x: int = span_x
        self.y: int = span_y
        self.index: int = 0
        self.moving = False
        self._image_cache: dict[str, tuple] = {}
        for frames in self._directions.values():
            for path in frames:
                self._image_cache[path] = mlx.mlx_png_file_to_image(
                    mlx_ptr,
                    str(path)
                )

    def update_img(self, direction: str) -> None:
        if direction != self._direction:
            self._direction = direction
        move = self._directions[self._direction]
        self._img_name = move[self.index % len(move)]
        self.img, self.img_width, self.img_height = self._image_cache[
            self._img_name
        ]
        self.index += 1

    def hit_gum(
        self,
        position: list,
        OFFSET_X: int,
        OFFSET_Y: int,
        CELL_W: int,
        CELL_H: int,
        m_w: int,
        m_h: int
    ) -> Union[tuple[int, int] | None]:
        center_x = self.x + self.img_width // 2
        center_y = self.y + self.img_height // 2

        col = (center_x - OFFSET_X) // CELL_W
        row = (center_y - OFFSET_Y) // CELL_H

        gum_x = OFFSET_X + col * CELL_W + (CELL_W - m_w) // 2
        gum_y = OFFSET_Y + row * CELL_H + (CELL_H - m_h) // 2

        if (gum_y, gum_x) in position:
            return gum_y, gum_x

        return None

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.img_width, self.img_height)
