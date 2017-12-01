from typing import List

from parsing.domain.symbol import Symbol
from parsing.domain.non_terminal import NonTerminal


class Rule:

    def __init__(self, left: NonTerminal, right: List[Symbol]):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "{} -> {}".format(str(self.left), "".join(str(symbol) for symbol in self.right))