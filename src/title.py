from characters import SpanningCharacter
from format import Alignment
from separator import Separator
from text import Text


class Title:
    def __init__(
        self,
        text: str,
        alignment: Alignment = Alignment.CENTER,
        ornament: SpanningCharacter = SpanningCharacter.BLANK,
        offset: int = 0,
        buffer: int = 1,
        surround: bool = False
    ):
        self.text = text
        self.alignment = alignment
        self.ornament = ornament
        self.offset = offset
        self.buffer = buffer
        self.surround = surround
    
    @staticmethod
    def _render_title_line(line: str, ornament: SpanningCharacter, alignment: Alignment, width: int) -> str:
        match alignment:
            case Alignment.LEFT:
                align = "<"
            case Alignment.RIGHT:
                align = ">"
            case Alignment.CENTER:
                align = "^"
            case _:
                raise ValueError(f"Unexpected alignment encountered. got: {alignment}")
        return f"{line:{ornament.value}{align}{width}}"

    def render(self, text_width: int = 24, width: int = 48) -> list[str]:
        title_lines = Text.build_lines(self.text, text_width)
        buffer = " " * self.buffer
        title_lines = [f"{buffer}{line}{buffer}" for line in title_lines]
        effective_width = width - self.offset * 2
        offset = " " * self.offset
        aligned_lines = [self._render_title_line(line, self.ornament, self.alignment, effective_width) for line in title_lines]
        rendered_lines = [offset + line + offset for line in aligned_lines]
        if self.surround:
            sep = Separator(self.ornament, offset=self.offset)
            rendered_lines = sep.render() + rendered_lines + sep.render()
        return rendered_lines


if __name__ == "__main__":
    t = Title("This is a longer title!!!", alignment=Alignment.LEFT, ornament=SpanningCharacter.DOUBLE_LINE, surround=True)
    for r in t.render():
        print(r)