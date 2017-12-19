from functools import reduce
from symtable import Symbol
from typing import List

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.parser.closure import Closure
from parsing.parser.parser_item import ParserItem
from parsing.state.incompatible_state_to_rule import IncompatibleStateToRuleException
from parsing.state.state_conflict import StateConflict


class State:

    def __init__(self, parse_items: List[ParserItem], grammar: ContextFreeGrammar):
        self._parse_items = parse_items
        self._grammar = grammar

    def go_to(self, with_symbol: Symbol):
        items = [x.go_next() for x in self._parse_items if x.next == with_symbol]
        extend = [Closure(item, self._grammar).closure() for item in items]
        return State([], self._grammar) if extend == [] \
            else State([item for sublist in extend for item in sublist], self._grammar)

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

    def __eq__(self, other):
        return False if other is None else len(set(self.items)) == len(set(self.items).union(set(other.items)))

    def __hash__(self):
        return self.__str__().__hash__()

    def __represents_rule_from(self, rules, index):
        return len([rule for rule in rules if self._parse_items[index].equals_rule(rule)]) == 1

    def is_last(self) -> bool:
        return len(self._parse_items) == 1 and self.__represents_rule_from(self._grammar.rules, index=0)

    def is_final(self) -> bool:
        return len(self._parse_items) == 1 and self.__represents_rule_from(self._grammar.extend().start_rules, index=0)

    def check_conflict(self):
        if len(self._parse_items) > 1 and \
                self.__check_if_at_least_one_represents_rule_from(self._grammar.extend().rules):
            raise StateConflict(self)
        return self

    def __check_if_at_least_one_represents_rule_from(self, rules):
        return True in [self.__represents_rule_from(rules, index) for index in range(0, len(self._parse_items))]

    def to_rule(self) -> bool:
        if not (self.is_last() or self.is_final()):
            raise IncompatibleStateToRuleException()
        return self._parse_items[0].to_rule()
