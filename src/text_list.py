from enum import Enum
from itertools import chain, zip_longest

from text import Text


class ListStyle(Enum):
    UNORDERED = "unordered"
    ORDERED = "ordered"
    CHECKLIST = "checklist"

class TextList:
    def __init__(
        self,
        items: list[str],
        style: ListStyle = ListStyle.UNORDERED,
        offset: int = 0,
        double_spaced: bool = False,
    ):
        self.items = items
        self.style = style
        self.offset = offset
        self.double_spaced = double_spaced
    
    @staticmethod
    def _build_bullets(count: int, style: ListStyle):
        match style:
            case ListStyle.UNORDERED:
                bullets = [" - " for _ in range(count)]
            case ListStyle.ORDERED:
                bullets = [f" {i}. " for i in range(1, count + 1)]
            case ListStyle.CHECKLIST:
                bullets = [" [ ] " for _ in range(count)]
        return bullets

    @staticmethod
    def _render_bullets(bullets: list[str], max_bullet_length: int) -> list[str]:
        return [f"{b: >{max_bullet_length}}" for b in bullets]

    @staticmethod
    def _build_element(bullet: str, item_lines: list[str], max_bullet_length: int) -> list[str]:
        bullet_filler = " " * max_bullet_length
        bullets_and_item_lines = zip_longest([bullet], item_lines, fillvalue=bullet_filler)
        return list(bullets_and_item_lines)

    def render(self, width: int = 48) -> list[str]:
        bullets = self._build_bullets(len(self.items), self.style)
        max_bullet_len = max([len(b) for b in bullets]) + self.offset
        rendered_bullets = self._render_bullets(bullets, max_bullet_len)
        text_width = width - max_bullet_len
        if text_width <= 0:
            raise ValueError(f"Total list width is too small to print. list_width={width}, max_bullet_length={max_bullet_len}")
        if self.double_spaced:
            self.items = [i + "\n\n" for i in self.items]
        rendered_items = [Text.build_lines(item, text_width) for item in self.items]
        bullets_and_items = zip(rendered_bullets, rendered_items)
        list_elements = chain(*[self._build_element(bullet, item, max_bullet_len) for bullet, item in bullets_and_items])
        rendered_elements = [b + i for b, i in list_elements]
        return rendered_elements


if __name__ == "__main__":
    items = [
        "one",
        "two",
        "three",
        "A longer element,\nwith multiple lines",
        "a short one",
        "a short one",
        "a short one",
        "a short one",
        "a short one",
        "a short one",
        "a short one",
    ]
    tl = TextList(items, ListStyle.ORDERED)
    for l in tl.render():
        print(l)
