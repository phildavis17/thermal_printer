from dataclasses import dataclass
from enum import StrEnum

# TODO: Add label

@dataclass
class BorderCharset:
    char_set: str
    
    def __post_init__(self) -> None:
        if len(self.char_set) != 6:
            raise ValueError(f"A border charset must have exactly 6 characters. Got {self.char_set}. len={len(self.char_set)}")

    @property
    def top_left(self):
        return self.char_set[0]
    
    @property
    def top_right(self):
        return self.char_set[1]
    
    @property
    def bottom_left(self):
        return self.char_set[2]
    
    @property
    def bottom_right(self):
        return self.char_set[3]
    
    @property
    def horizontal(self):
        return self.char_set[4]
    
    @property
    def vertical(self):
        return self.char_set[5]


class BorderStyle(StrEnum):
    LINE = "┌┐└┘─│"
    DOUBLE_LINE = "╔╗╚╝═║"
    DOUBLE_HORIZONTAL = "╒╕╘╛═│"
    DOUBLE_VERTICAL = "╓╖╙╜─║"
    BLANK = "      "
    BLOCK_0 = "░░░░░░"
    BLOCK_1 = "▒▒▒▒▒▒"
    BLOCK_2 = "▓▓▓▓▓▓"
    BLOCK_3 = "██████"
    CORNER_LINES = "┌┐└┘  "
    CORNER_STARS = "****  "


class Border:
    def __init__(self, style: BorderStyle = BorderStyle.LINE):
        self.charset = BorderCharset(style)
    
    @staticmethod
    def _build_top_row(charset: BorderCharset, width: int) -> str:
        center_span = width - 2
        return charset.top_left + (charset.horizontal * center_span) + charset.top_right

    @staticmethod
    def _build_bottom_row(charset: BorderCharset, width: int) -> str:
        center_span = width - 2
        return charset.bottom_left + (charset.horizontal * center_span) + charset.bottom_right

    @staticmethod
    def _build_vertical_span(charset: BorderCharset) -> list[str]:
        return charset.vertical * 2

    def render(self, width: int = 48):
        if width < 3:
            raise ValueError("Borders cannot be rendered below 3 characters wide")
        return (
            self._build_top_row(self.charset, width),
            self._build_vertical_span(self.charset),
            self._build_bottom_row(self.charset, width),
        )


if __name__ == "__main__":
    b = Border(style=BorderStyle.DOUBLE_LINE)
    for e in b.render():
        print(e)