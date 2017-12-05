from symtable import Symbol
from functools import reduce
from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.parser.closure import Closure
from typing import List
from parsing.parser.item import ParserItem


class State:

    def go_to(self, with_symbol: Symbol):
        items = [x.go_next() for x in self._parse_items if x.next == with_symbol]
        extend = [Closure(item, self._grammar).closure() for item in items]
        return State([], self._grammar) \
            if extend == [] \
            else State(reduce(lambda x, y: x.union(y), extend), self._grammar)

    def __init__(self, parse_items: List[ParserItem], grammar: ContextFreeGrammar):
        self._parse_items = parse_items
        self._grammar = grammar

    @property
    def items(self) -> List[ParserItem]:
        return self._parse_items

    def __str__(self):
        return "\n".join(map(lambda x: str(x), self._parse_items))

