from typing import List

from parsing.domain.symbol import Symbol
from parsing.domain.non_terminal import NonTerminal


class Rule:

    def __init__(self, left: NonTerminal, right: List[Symbol]):
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return "{} -> {}".format(str(self.left), "".join(str(symbol) for symbol in self.right))
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    @staticmethod
    def from_string(string: str):
        result = string.replace(' ', '').split('->')
        return Rule(NonTerminal(result[0]), [Symbol(x) for x in result[1]])

    @staticmethod
    def from_complex_string(string: str):
        result = string.split(' -> ')
        return Rule(NonTerminal(result[0].replace(' ', '')),
                    [Symbol(x) for x in Rule.__get_symbols_from_string(result)])

    @staticmethod
    def __get_symbols_from_string(result):
        return ['ε'] if result[1].split(' ') == [''] else result[1].split(' ')

    @staticmethod
    def from_parser_item(parser_item):
        return Rule(parser_item.left, parser_item.right.all_symbols)
