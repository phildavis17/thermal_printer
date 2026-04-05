from format import Width48

from text import Text
from text_list import TextList
from separator import Separator
from title import Title
from border import Border, BorderStyle

type Content = Text | TextList | Separator | Title | Field

class Field:
    def __init__(
        self,
        content: Content,
        width: int,
        border: Border | None = None,
    ):
        self.content = content
        self.width = width
        self.border = border

    @staticmethod
    def _add_border(content: list[str], border: Border | None, width: int):
        if border is None:
            return content
        top, vertical_span, bottom = border.render(width)
        left, right = vertical_span
        content = [left + line + right for line in content]
        content = [top] + content + [bottom]
        return content

    def render(self) -> list[str]:
        border_width = 2 if self.border is not None else 0
        content_width = self.width - border_width
        rendered_content = self.content.render(width=content_width)
        content_with_border = self._add_border(rendered_content, self.border, self.width)
        return content_with_border


if __name__ == "__main__":
    width = Width48.QUARTER
    b = Border(BorderStyle.DOUBLE_LINE)
    t = Text("This is a test of a field.\nSecond line\nLoooooooooooooooooooooooooooooooooooooooooooooooooooooooong")
    f = Field(t, Width48.QUARTER, b)

    for line in f.render():
        print(line)