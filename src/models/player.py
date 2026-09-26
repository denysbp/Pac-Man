from typing import Any, Union
from .metadata import Rect
from .configs import (
    RIGHT, LEFT, TOP, DOWN
)
from mlx.mlx import Mlx


class Player:
    """
    Responsible for managing the player position, movement direction,
    lives and animation images

    Attributes
    __________
    _img_name: str
        store the name of the current player image
    _direction: str
        store the current movement direction
    live: int
        store the number of lives of the player
    img: Any
        store the current player image
    img_width: int
        represent the width of the current player image
    img_height: int
        represent the height of the current player image
    _directions: dict[str, list]
        store the image frames associated with each direction
    x: int
        represent the horizontal position of the player
    y: int
        represent the vertical position of the player
    index: int
        store the current animation frame index
    moving: bool
        indicate whether the player is moving
    _image_cache: dict[str, tuple]
        store the loaded images for each player animation frame

    Methods
    _______
    update_img():
        update the player image according to the current direction
    hit_gum():
        check if the player is currently touching a gum
    rect:
        return a rectangle representing the player position and size
    """
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
        """
        Update the player image for the given direction

        Args:
            direction: str
                represent the direction in which the player is moving
        """
        if direction != self._direction:
            self._direction = direction
        move = self._directions[self._direction]
        self._img_name = move[self.index % len(move)]
        self.img, self.img_width, self.img_height = self._image_cache[
            self._img_name
        ]
        self.index += 1
        if self.index > 100:
            self.index = 0

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
        """
        Check if the player is currently touching a gum
        Args:
            position: list
                store the positions of the available gums
            OFFSET_X: int
                represent the horizontal offset of the map
            OFFSET_Y: int
                represent the vertical offset of the map
            CELL_W: int
                represent the width of a map cell
            CELL_H: int
                represent the height of a map cell
            m_w: int
                represent the width of the gum
            m_h: int
                represent the height of the gum

        Returns:
            tuple[int, int] | None
                return the position of the gum if the player is touching it,
                otherwise return None
        """
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
        """Return the rect for the player"""
        return Rect(self.x, self.y, self.img_width, self.img_height)
