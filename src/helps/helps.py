from typing import TYPE_CHECKING, Any
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
) -> bool:
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


def put_pixel(
    data: Any,
    size_line: int,
    x: int,
    y: int,
    color: int
) -> None:
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
    # we catch the 8 fisrt bits
    data[offset + 1] = (color >> 8) & 0xFF
    data[offset + 2] = (color >> 16) & 0xFF
    data[offset + 3] = (color >> 24) & 0xFF
    # write the 4 bytes of the color on the pixel


def drawlineH(
    data: Any,
    size_line: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int
) -> None:
    """
    Draws a line between two points using an error-based algorithm.

    The function assumes that the line is mostly horizontal, meaning
    the distance on the x-axis is greater than the distance on the
    y-axis. The error value is used to decide when the y coordinate
    needs to be changed while moving through the x coordinates.

    If the first point is to the right of the second point, the
    coordinates are swapped so that the line is always processed
    from left to right. The direction of the y coordinate is kept
    separately to support lines going upwards or downwards.

    Args:
        data: Image memory buffer where the pixels are written.
        size_line: Number of bytes occupied by one image row.
        x0: Horizontal coordinate of the first point.
        y0: Vertical coordinate of the first point.
        x1: Horizontal coordinate of the second point.
        y1: Vertical coordinate of the second point.
        color: 32-bit integer representing the color of the line.

    Returns:
        None.
    """
    # we decide the correct position to start
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
        p = 2 * dy - dx
        for i in range(dx + 1):
            put_pixel(data, size_line, x0 + i, y, color)
            if p >= 0:
                y += dt
                # if the error is to big we need to change one unity in dy
                p = p - 2 * dx
            # then we correct the error again
            p = p + 2*dy


def drawlineV(
    data: Any,
    size_line: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: int
) -> None:
    """
    Draws a vertical line between two points using an error-based
    line drawing algorithm.

    The function assumes that the line is mostly vertical, so the
    y coordinate is increased one pixel at a time. The error value
    is used to decide when the x coordinate needs to be changed.

    If the first point is below the second point, the coordinates
    are swapped so that the line is always processed from top to
    bottom. The direction of the x coordinate is kept separately
    so the line can go either left or right.

    Args:
        data: Image memory buffer where the pixels are written.
        size_line: Number of bytes occupied by one image row.
        x0: Horizontal coordinate of the first point.
        y0: Vertical coordinate of the first point.
        x1: Horizontal coordinate of the second point.
        y1: Vertical coordinate of the second point.
        color: 32-bit integer representing the color of the line.

    Returns:
        None.
    """
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
                p = p - 2 * dy
            p = p + 2 * dx


def blit_into_buffer(
    dst_data: Any,
    dst_bpp: int,
    dst_size_line: int,
    dst_w: int,
    dst_h: int,
    src_data: Any,
    src_bpp: int,
    src_size_line: int,
    src_w: int,
    src_h: int,
    dst_x: int,
    dst_y: int
) -> None:
    """
    Copies an image from one memory buffer into another.

    The source image is copied pixel by pixel starting at the given
    destination coordinates. Pixels that fall outside the destination
    image are ignored.

    The function uses the alpha component of each source pixel to
    determine whether it should be copied. Fully transparent pixels
    are skipped, while visible pixels are converted into a 32-bit
    color before being written to the destination buffer.

    The source and destination images can have different dimensions
    and bytes-per-pixel values. The row size of each image is used
    to calculate the position of each pixel in its respective memory
    buffer.

    Args:
        dst_data: Destination image memory buffer.
        dst_bpp: Number of bits used by each destination pixel.
        dst_size_line: Number of bytes occupied by one destination row.
        dst_w: Width of the destination image in pixels.
        dst_h: Height of the destination image in pixels.
        src_data: Source image memory buffer.
        src_bpp: Number of bits used by each source pixel.
        src_size_line: Number of bytes occupied by one source row.
        src_w: Width of the source image in pixels.
        src_h: Height of the source image in pixels.
        dst_x: Horizontal position where the source image is placed.
        dst_y: Vertical position where the source image is placed.

    Returns:
        None. The destination image buffer is modified directly.
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
            # we construct the color with (or) to agrupate everything
            color = (
                src_data[src_offset] |
                (src_data[src_offset + 1] << 8) |
                (src_data[src_offset + 2] << 16) |
                (src_data[src_offset + 3] << 24)
            )
            put_pixel(dst_data, dst_size_line, px, py, color)
