from typing import TYPE_CHECKING, Any
from mlx.mlx import Mlx
if TYPE_CHECKING:
    from ..models import Player

def colision(
    player: "Player",
    WIDTH: int,
    HEIGHT: int,
    V: int,
    H: int
):
    player = player.rect
    if ((player.left + V) < 0 or
        (player.right - V) > WIDTH or
        (player.top - H) < 0 or
        (player.bottom - H) > HEIGHT
    ):
        return True
    return False


def drawlineH(x0, y0, x1, y1, mlx: Mlx, mlx_ptr: Any, window: Any):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    dt = -1 if dy < 0 else 1

    dy *= dt

    if dx != 0:
        y = y0
        p = 2*dy - dx
        for i in range(dx + 1):
            mlx.mlx_pixel_put(mlx_ptr, window, x0 + i, y)
            if p >= 0:
                y += dt
                p = p - 2*dx
            p = p + 2*dy


def drawlineV(x0, y0, x1, y1, mlx: Mlx, mlx_ptr: Any, window: Any):
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    dt = -1 if dy < 0 else 1

    dy *= dt

    if dx != 0:
        y = y0
        p = 2*dy - dx
        for i in range(dx + 1):
            mlx.mlx_pixel_put(mlx_ptr, window, x0 + i, y)
            if p >= 0:
                y += dt
                p = p - 2*dx
            p = p + 2*dy
