from parsing.parser.position import ParserPosition
from parsing.domain.non_terminal import NonTerminal
from parsing.domain.symbol import Symbol


class ParserItem:

    def __init__(self, left: NonTerminal, right: ParserPosition):
        self._left = left
        self._right = right

    @property
    def right(self) -> ParserPosition:
        return self._right

    @property
    def left(self) -> NonTerminal:
        return self._left

    @property
    def next(self) -> Symbol:
        return self._right.left[0]

    @property
    def has_next(self) -> bool:
        return len(self._right.left) > 0

    @staticmethod
    def item_for(rule):
        return ParserItem(rule.left, ParserPosition([], rule.right))

    def go_next(self):
        return ParserItem(self._left, self._right.go_next())

    def is_final(self):
        return self._right.is_final()

    @staticmethod
    def from_string(string: str):
        result = string.replace(' ', '').split('->')
        visited, left = result[1].split('.')
        return ParserItem(NonTerminal(result[0]),
                          ParserPosition([Symbol(x) for x in visited],
                                         [Symbol(x) for x in left]))

    def __eq__(self, other):
        return self.right == other.right and self._left == other.left

    def __str__(self):
        return "{} -> {}".format(str(self._left), str(self._right))

    def __eq__(self, ot):
        return self.__str__() == str(ot)

    def __hash__(self):
        return self.__str__().__hash__()

