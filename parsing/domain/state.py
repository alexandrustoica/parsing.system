from symtable import Symbol
from functools import reduce
from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.parser.closure import Closure
from typing import List
from parsing.parser.item import ParserItem


class State:

    def __init__(self, parse_items: List[ParserItem], grammar: ContextFreeGrammar):
        self._parse_items = parse_items
        self._grammar = grammar

    def go_to(self, with_symbol: Symbol):
        items = [x.go_next() for x in self._parse_items if x.next == with_symbol]
        extend = [Closure(item, self._grammar).closure() for item in items]
        return State([], self._grammar) \
            if extend == [] \
            else State(reduce(lambda x, y: x.union(y), extend), self._grammar)

    @property
    def items(self) -> List[ParserItem]:
        return self._parse_items

    @property
    def is_valid(self):
        return len(self._parse_items) > 0

    def __str__(self):
        return "\n".join(map(lambda x: str(x), self._parse_items))

    def __repr__(self):
        return ", ".join(map(lambda x: str(x), self._parse_items))

    def __eq__(self, ot):
        self_set = set(self.items)
        init_len = len(self_set)
        return init_len == len(self_set.union(set(ot.items)))

    def __hash__(self):
        return self.__str__().__hash__()

    def _represents_rule_from(self, rules):
        return len(self._parse_items) == 1 and \
               len([rule for rule in rules if self._parse_items[0].equals_rule(rule)]) == 1

    def is_last(self) -> bool:
        return self._represents_rule_from(self._grammar.rules)

    def is_final(self) -> bool:
        return self._represents_rule_from(self._grammar.extend().start_rules)
