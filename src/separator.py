from enum import Enum

from characters import SpanningCharacter

class SepChar(Enum):
    DASH = "-"
    EQUALS = "="
    UNDERSCORE = "_"
    LINE = "─"
    DOUBLE_LINE = "═"
    BLOCK_0 = "░"
    BLOCK_1 = "▒"
    BLOCK_2 = "▓"
    BLOCK_3 = "█"
    BLOCK_LOWER = "▄"
    BLOCK_UPPER = "▀"
    BLANK = " "
    STAR = "*"
    TILDE = "~"


class Separator:
    def __init__(self, char: SpanningCharacter = SpanningCharacter.LINE, offset: int = 0):
        self.char = char
        self.offset = offset

    def render(self, width: int = 48) -> list[str]:
        rendered_offset = self.offset
        if rendered_offset * 2 > width:
            rendered_offset = 0
        buffer = " " * rendered_offset    
        return [buffer + self.char.value * (width - rendered_offset * 2) + buffer]


if __name__ == "__main__":
    s = Separator(char=SpanningCharacter.STAR)
    for r in s.render():
        print(r)