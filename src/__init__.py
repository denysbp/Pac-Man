from .models import(
    Player,
    ConfigData,
    Level,
    Memory,
    Rect,
    alocate_levels,
    create_config
)
keyboard: dict[str, int] = {
    65509: "capslock!",
    97: "a",
    98: "b",
    99: "c",
    100: "d",
    101: "e",
    102: "f",
    103: "g",
    104: "h",
    105: "i",
    106: "j",
    107: "k",
    108: "l",
    109: "m",
    110: "n",
    111: "o",
    112: "p",
    113: "q",
    114: "r",
    115: "s",
    116: "t",
    117: "u",
    118: "v",
    119: "w",
    120: "x",
    121: "y",
    122: "z",
    32: " "
}
from .loader import LoaderError, ConfigLoader, ScoreSpriteGenerator
from .helps import (
    colision,
    drawlineH,
    drawlineV,
    put_pixel,
    blit_into_buffer
)
from .ui import Render
from .data_base import DATA_BASE