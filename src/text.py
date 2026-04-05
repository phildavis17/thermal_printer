import itertools
import textwrap
from format import Alignment

class Text:
    def __init__(self, contents: str, alignment: Alignment = Alignment.LEFT):
        self.contents = contents
        self.alignment = alignment
    
    @staticmethod
    def build_lines(text: str, width: int) -> str:
        graphs = text.splitlines(keepends=True)
        wrapped = [textwrap.wrap(g, width, drop_whitespace=False) for g in graphs]
        return [line for line in itertools.chain(*wrapped)]
    
    def render(self, width: int = 48) -> list[str]:
        match self.alignment:
            case Alignment.LEFT:
                align = "<"
            case Alignment.RIGHT:
                align = ">"
            case Alignment.CENTER:
                align = "^"
        lines = self.build_lines(self.contents, width)
        return [f"{line: {align}{width}}" for line in lines]


if __name__ == "__main__":
    test_text_0 = "this is a test."
    test_text_1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, \nsed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    test_text_2 = """Now that I'm happy, I think of when I was not.
The angles of the city gave the impression of happiness,

the torquing El, the tourist sculpture 
like a globe shimmying through a looking-glass sock.

Late one night, from his illumined image on a grid,
the stranger in the high-rise summoned me

for an act so angular I became the neck 
of the crepuscular swan that Cornell glued into a box. 

The next day I stood in front of the vitrine 
at the museum, willing away my own reflection 

to inhabit a clock, a dovecote, 
a bubble that would never pop.

Across the country I'd idly refresh his screens, 
the young doctor in dignified poses

at the pediatric oncology ward 
or alluring ones above Michigan Avenue, 

at first alone, then with another, grinning 
like reunited twins, until their journey 

mirrored our own updates: a sensuous ryokan, 
a waterfall guttering in an antipodal fjord, 

matching tuxedos in a canted archway 
at some timeless villa rustica.
"""
    t = Text(test_text_1)
    for row in t.render():
        print(row)