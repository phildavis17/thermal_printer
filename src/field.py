from characters import SpanningCharacter
from format import Width48
from text import Text
from text_list import TextList, ListStyle
from separator import Separator
from title import Title
from border import Border, BorderStyle

type Content = Text | TextList | Separator | Title | Field
type Row = Content | list[Content]

class Field:
    def __init__(
        self,
        content: list[Row],
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

    @staticmethod
    def _pad_content_lines(lines: list[str], target_len: int) -> list[str]:
        line_len = len(lines[0])
        while len(lines) < target_len:
            lines.append(" " * line_len)
        return lines

    @staticmethod
    def _flatten_contents(padded_contents: list[list[str]]) -> list[str]:
        flat_lines = []
        for line in zip(*padded_contents):
            flat_lines.append("".join(line))
        return flat_lines

    def _get_effective_rendering_width(self, specified_width: int | None) -> int:
        if specified_width is not None:
            max_width = min(specified_width, self.width)
        else:
            max_width = self.width
        border_width = 2 if self.border is not None else 0
        effective_width = max_width - border_width
        return effective_width, border_width

    def _render_columns(self, columns: list[Content], width: int) -> list[str]:
        specified = [(i, c.width) for i, c in enumerate(columns) if hasattr(c, "width")]
        flex_indices = [i for i, c in enumerate(columns) if not hasattr(c, "width")]
        total_specified = sum(w for _, w in specified)

        col_widths: dict[int, int] = {}
        if total_specified > width:
            remaining = width
            for j, (i, w) in enumerate(specified):
                if j == len(specified) - 1:
                    col_widths[i] = max(1, remaining)
                else:
                    allocated = max(1, round(w / total_specified * width))
                    col_widths[i] = allocated
                    remaining -= allocated
            for i in flex_indices:
                col_widths[i] = 0
        else:
            flex_count = len(flex_indices)
            flex_width = (width - total_specified) // flex_count if flex_count > 0 else 0
            for i, w in specified:
                col_widths[i] = w
            for i in flex_indices:
                col_widths[i] = flex_width

        rendered_columns = [c.render(col_widths[i]) for i, c in enumerate(columns)]
        max_len = max(len(rc) for rc in rendered_columns)
        padded = [self._pad_content_lines(rc, max_len) for rc in rendered_columns]
        flat = self._flatten_contents(padded)
        return [line.ljust(width) for line in flat]

    def _render_row(self, row: Row, width: int) -> list[str]:
        if isinstance(row, list):
            return self._render_columns(row, width)
        return row.render(width)

    def render(self, width: int | None = None) -> list[str]:
        effective_width, border_width = self._get_effective_rendering_width(width)
        rendered_rows = [self._render_row(row, effective_width) for row in self.content]
        rendered_content = [line for row in rendered_rows for line in row]
        return self._add_border(rendered_content, self.border, effective_width + border_width)


if __name__ == "__main__":
    b = Border(BorderStyle.DOUBLE_HORIZONTAL)
    t = Text("This is a test of a field.\nSecond line\nLoooooooooooooooooooooooooooooooooooooooooooooooooooooooong")
    f1 = Field([Text("This is the first text")], Width48.QUARTER, Border(BorderStyle.CORNER_LINES))
    f2 = Field(
        [
            Title("A list."),
            TextList(["first", "second"], ListStyle.CHECKLIST, double_spaced=True),
        ],
        Width48.HALF,
        Border(BorderStyle.DOUBLE_LINE),
    )
    fill_text = Text(" ")
    f = Field(
        [
            Title("Header", ornament=SpanningCharacter.LINE, offset=2),
            Separator(SpanningCharacter.BLANK),
            [f1, fill_text, f2],
            Separator(SpanningCharacter.BLANK),
            t,
            Separator(SpanningCharacter.BLANK),
        ],
        Width48.FULL,
        b,
        )
    for l in f.render():
        print(l)
