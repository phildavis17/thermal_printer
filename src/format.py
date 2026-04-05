from enum import Enum, IntEnum
from dataclasses import dataclass

class Alignment(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


class Underline(Enum):
    NONE = 0
    FAINT = 1
    STRONG = 2


class Width48(IntEnum):
    FULL = 48
    HALF = 24
    THIRD = 16
    QUARTER = 12
    SIXTH = 8
    EIGHTH = 6
    TWELFTH = 4
    SIXTEENTH = 3

@dataclass
class FormatParams:
    algignment: Alignment
    bold: bool
    underline: Underline
    invert: bool


class ImageImpl(Enum):
    RASTER = "bitImageRaster"
    GRAPHICS = "graphics"
    COLUMN = "bitImageColumn"

