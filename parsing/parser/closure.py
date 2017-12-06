from typing import List

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.parser.item import ParserItem
from parsing.domain.symbol_type import SymbolType


class Closure:

    def __init__(self, item: ParserItem, grammar: ContextFreeGrammar):
        self._item = item
        self._grammar = grammar

    def closure(self) -> List[ParserItem]:
        result = [self._item]
        accumulator = [self._item]
        while accumulator:
            for item in accumulator:
                if item.has_next:
                    for rule in self._grammar.rules_of(item.next):
                        if ParserItem.item_for(rule) not in result:
                            accumulator.append(ParserItem.item_for(rule))
                            result.append(ParserItem.item_for(rule))
                accumulator.remove(item)
        return result

    @staticmethod
    def _filter_next_non_terminal(source: List[ParserItem]) -> List[ParserItem]:
        return list(filter(lambda item: item.next.type == SymbolType.NON_TERMINAL, source))
