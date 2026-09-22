from typing import TYPE_CHECKING, Any
from mlx.mlx import Mlx
if TYPE_CHECKING:
    from ..models import Player

def colision(
    player: "Player",
    left: int,
    right: int,
    top: int,
    bottom: int,
    colision_bot_player: bool = False,
    invecibility: bool = False
):
    if colision_bot_player:
        if invecibility:
            return True
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

def put_pixel(data, size_line, x, y, color):
    """
        Draws a pixel directly into an image memory buffer.

        Args:
            data: Image memory buffer where the pixel will be written.
            size_line: Number of bytes occupied by one image row.
            x: Horizontal coordinate of the pixel.
            y: Vertical coordinate of the pixel.
            color: 32-bit integer representing the pixel color.

        The pixel position is calculated using the row size and the
        number of bytes occupied by each pixel. The color is then
        split into four bytes and written individually into the buffer.
    """
    # find the pixel
    offset = y * size_line + x * 4

    data[offset] = color & 0xFF
    data[offset + 1] = (color >> 8) & 0xFF
    data[offset + 2] = (color >> 16) & 0xFF
    data[offset + 3] = (color >> 24) & 0xFF
    # write the 4 bytes of the color on the pixel

def drawlineH(data, size_line, x0, y0, x1, y1, color):
    # we decide the correect position to start
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # we decide how far we will walk
    dx = x1 - x0
    dy = y1 - y0

    dt = -1 if dy < 0 else 1

    dy *= dt

    if dx != 0:
        y = y0
        # line approximation error
        p = 2*dy - dx
        for i in range(dx + 1):
            put_pixel(data, size_line, x0 + i, y, color)
            if p >= 0:
                y += dt
                # if the error is to big we need to change one unity in dy
                p = p - 2*dx
            # then we correct the error again
            p = p + 2*dy


def drawlineV(data, size_line, x0, y0, x1, y1, color):
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
            put_pixel(data, size_line, x, y0 + i, color)
            if p >= 0:
                x += dt
                p = p - 2*dy
            p = p + 2*dx

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

    """
    Copies a source image into a destination image buffer.

    The source image is placed at the given destination coordinates.
    Pixels outside the destination boundaries are ignored.

    Transparent source pixels are skipped using their alpha value.
    Each visible pixel is converted into a 32-bit color and written
    directly into the destination buffer.
    this function copy only 1 pixel per iteration
    """
    src_bytes_per_pixel = src_bpp // 8
    for row in range(src_h):
        # where that line gonna be on dst
        py = dst_y + row
        # check if its out-side off the buffer
        if py < 0 or py >= dst_h:
            continue
        for col in range(src_w):
            # find the x on dst
            px = dst_x + col
            if px < 0 or px >= dst_w:
                continue
            # Find the position off (col, row ) inside the the memory (src)
            src_offset = row * src_size_line + col * src_bytes_per_pixel
            # find the alpha (transparency)
            alpha = src_data[src_offset + 3]
            if alpha == 0:
                continue
            # we construct the color with or to agrupate everything
            color = (
                src_data[src_offset] |
                (src_data[src_offset + 1] << 8) |
                (src_data[src_offset + 2] << 16) |
                (src_data[src_offset + 3] << 24)
            )
            put_pixel(dst_data, dst_size_line, px, py, color)