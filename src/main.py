from characters import SpanningCharacter
from format import Alignment, Width48
from text import Text
from text_list import TextList, ListStyle
from separator import Separator
from title import Title
from border import Border, BorderStyle
from field import Content, Row, Field
from thermal import ConfiguredPrinter, PrintJob, get_configured_printer


if __name__ == "__main__":
    unordered_list = TextList(
        [
            "One",
            "Two",
            "Three",
        ],
        style=ListStyle.UNORDERED,
    )
    ordered_list = TextList(
        [
            "Four",
            "Five",
            "Six",
        ],
        style=ListStyle.ORDERED,
    )
    check_list = TextList(
        [
            "Seven",
            "Eight",
            "Nine",
        ],
        style=ListStyle.CHECKLIST,
    )
    list_title = Title("Three kinds of lists", ornament=SpanningCharacter.TILDE, offset=2)
    list_demo = Field(
        [
            list_title,
            [unordered_list, ordered_list, check_list],
        ],
        Width48.FULL,
        border=Border(),
    )
    intro_title = Title("Hello, Madeleine", ornament=SpanningCharacter.BLOCK_3, surround=True, buffer=3)
    blank_line = Separator(SpanningCharacter.BLANK)
    intro = Text(
        "This is a demo of the stuff I've been working on with the thermal printer."
        "Here are examples of some of the stuff it can do."
    )
    intro_field = Field(
        [
            intro_title,
            blank_line,
            blank_line,
            intro,
        ],
        Width48.FULL,
    )

    title_demo = Field(
        [
            Title("Titles"),
            blank_line,
            Title("With Various Ornamentation", ornament=SpanningCharacter.STAR),
            Title("That Can Be Offset"),
            Title("From the Edge", ornament=SpanningCharacter.TILDE, offset=5),
            Title("Or"),
            Title("From the Text", ornament=SpanningCharacter.TILDE, buffer=5),
            Title("And Can Handle\nMulti-Line Text", ornament=SpanningCharacter.DASH),

        ],
        width=Width48.FULL,
    )

    separator_demo = Field(
        [
            Title("Many kinds of Separators"),
            Separator(SpanningCharacter.STAR),
            Separator(SpanningCharacter.DASH),
            Separator(SpanningCharacter.EQUALS),
            Separator(SpanningCharacter.LINE),
            Separator(SpanningCharacter.DOUBLE_LINE),
            Separator(SpanningCharacter.BLOCK_0),
            Separator(SpanningCharacter.BLOCK_1),
            Separator(SpanningCharacter.BLOCK_2),
            Separator(SpanningCharacter.BLOCK_3),
        ],
        width=Width48.FULL,
    )

    justification_demo = Field(
        [
            Title("Text Can Be Aligned", ornament=SpanningCharacter.LINE),
            Text("To the left"),
            Text("or centered", alignment=Alignment.CENTER),
            Text("or to the right.", alignment=Alignment.RIGHT),
        ],
        Width48.FULL,
    )

    left_column = Field(
        [
            Separator(SpanningCharacter.BLOCK_1),
            Text("If you specify a width, the column will try to limit itself to that width, and wrap its contents accordingly"),
            Separator(SpanningCharacter.BLOCK_1),
        ],
        Width48.QUARTER,
        border=Border(BorderStyle.CORNER_LINES),
    )
    right_column = Field(
        [
            Text("And fields with unspecified widths will determine their own widths using the remaining space."),
        ],
        border=Border(BorderStyle.DOUBLE_LINE),
        width=Width48.FULL - Width48.QUARTER,
    )


    columns_demo = Field(
        [
            Title("Any Element Can Be Arranged\n In Arbitrary Fields"),
            [left_column, right_column]
        ],
        border=Border(BorderStyle.DOUBLE_HORIZONTAL),
        width=Width48.FULL
    )

    closing_text = Field(
        [
            Text("And as of this morning, there's a way to turn all this into an actual printable format, and send it to the printer. There's a lot more work to do until this is actually useful for anything, but this is progress."),
            Title("I love you!", surround=True),
        ],
        width=Width48.FULL,
    )

    full_demo = Field(
        [
            intro_field,
            blank_line,
            title_demo,
            blank_line,
            separator_demo,
            blank_line,
            justification_demo,
            blank_line,
            list_demo,
            blank_line,
            columns_demo,
            blank_line,
            closing_text,
        ],
        width=Width48.FULL
    )


    p = get_configured_printer()
    pj = PrintJob(full_demo.render())
    p.send_job(pj)
    # for l in full_demo.render():
    #     print(l)