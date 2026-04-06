from itertools import zip_longest
from typing import get_args

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
        content: Content | list[Content],
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
    
    def _pad_content_lines(lines: list[str], target_len: int) -> list[str]:
        line_len = len(lines[0])
        while len(lines) < target_len:
            lines.append(" " * line_len)
    
    def _flatten_contents(self, content_width: int):
        # TODO: add column separation using join character.
        #       adjust widths accordingly. Have to handle exceeded limits
        if not isinstance(self.content, list):
            return self.content
        specified_widths = [c.width for c in self.content if hasattr(c, "width")]
        total_flex_width = content_width - sum(specified_widths)
        flex_width = total_flex_width // (len(self.content) - len(specified_widths))
        rendered_contents = []
        for c in self.content:
            c_width = c.width if hasattr(c, "width") else flex_width
            rendered_contents.append(c.render(c_width))
        max_content_length = max([len(rc) for rc in rendered_contents])
        # TODO: I've made a hash of this lengthening stuff. Gotta fix it.
        #       desired end state is that each sub-content is as long as the longest one
        #       have not successfully handled situation where there's only one content.
        lengthened_content = []
        for rc in rendered_contents:
            if len(rc) < max_content_length:
                lc = self._pad_content_lines(rc), max_content_length
            else:
                lc = rc
            lengthened_content.append(lc)
        return Text("".join(["".join(line) for line in zip_longest(*lengthened_content, fillvalue="")]))
        


    def render(self, width: int | None = None) -> list[str]:
        if width is not None:
            field_width = min(self.width, width)
        else:
            field_width = self.width
        border_width = 2 if self.border is not None else 0
        content_width = field_width - border_width
        self.content = self._flatten_contents(content_width)
        rendered_content = self.content.render(width=content_width)
        content_with_border = self._add_border(rendered_content, self.border, self.width)
        return content_with_border


if __name__ == "__main__":
    width = Width48.QUARTER
    b = Border(BorderStyle.DOUBLE_LINE)
    t = Text("This is a test of a field.\nSecond line\nLoooooooooooooooooooooooooooooooooooooooooooooooooooooooong")
    f1 = Field(Text("This is the first text"), Width48.HALF, Border())
    f = Field([f1, t], Width48.FULL, b)
    for l in f.render():
        print(l)