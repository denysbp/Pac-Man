from typing import TYPE_CHECKING, Any
from mlx.mlx import Mlx
from math import cos, sin, radians
if TYPE_CHECKING:
    from ..models import Player

def colision(
    player: "Player",
    left: int,
    right: int,
    top: int,
    bottom: int,
    V: int = 0,
    H: int = 0
):
    rect = player.rect

    if rect.left < left:
        return True

    if rect.right > right:
        return True

    if rect.top < top:
        return True

    if rect.bottom > bottom:
        return True

    return False

def put_pixel(data, bpp, size_line, x, y, color):
    offset = y * size_line + x * 4

    data[offset] = color & 0xFF
    data[offset + 1] = (color >> 8) & 0xFF
    data[offset + 2] = (color >> 16) & 0xFF
    data[offset + 3] = (color >> 24) & 0xFF

def drawlineH(data, bpp, size_line, x0, y0, x1, y1, color):
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
            put_pixel(data, bpp, size_line, x0 + i, y, color)
            if p >= 0:
                y += dt
                p = p - 2*dx
            p = p + 2*dy


def drawlineV(data, bpp, size_line, x0, y0, x1, y1, color):
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    dt = -1 if dx < 0 else 1
    dx *= dt

    if dy != 0:
        x = x0
        p = 2*dx - dy
        for i in range(dy + 1):
            put_pixel(data, bpp, size_line, x, y0 + i, color)
            if p >= 0:
                x += dt
                p = p - 2*dy
            p = p + 2*dx

def drawline(
    data,
    bpp,
    size_line,
    x0,
    y0,
    x1,
    y1,
    color
):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    error = dx - dy

    while True:
        put_pixel(
            data,
            bpp,
            size_line,
            x0,
            y0,
            color
        )

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * error

        if e2 > -dy:
            error -= dy
            x0 += sx

        if e2 < dx:
            error += dx
            y0 += sy


def blit_into_buffer(
    dst_data,
    dst_bpp,
    dst_size_line,
    dst_w,
    dst_h,
    src_data,
    src_bpp,
    src_size_line,
    src_w,
    src_h,
    dst_x,
    dst_y
):
    src_bytes_per_pixel = src_bpp // 8
    for row in range(src_h):
        py = dst_y + row
        if py < 0 or py >= dst_h:
            continue
        for col in range(src_w):
            px = dst_x + col
            if px < 0 or px >= dst_w:
                continue
            src_offset = row * src_size_line + col * src_bytes_per_pixel
            alpha = src_data[src_offset + 3]
            if alpha == 0:
                continue
            color = (
                src_data[src_offset] |
                (src_data[src_offset + 1] << 8) |
                (src_data[src_offset + 2] << 16) |
                (src_data[src_offset + 3] << 24)
            )
            put_pixel(dst_data, dst_bpp, dst_size_line, px, py, color)
