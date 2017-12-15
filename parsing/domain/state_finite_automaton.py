from typing import List

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.domain.state import State
from parsing.domain.state_table_element import StateTableElement
from parsing.parser.closure import Closure
from parsing.parser.item import ParserItem


class StateFiniteAutomaton:

    def __init__(self, grammar: ContextFreeGrammar):
        self.__grammar = grammar
        extended = self.__grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("E"))[0])
        items = Closure(item, extended).closure()
        self.__start = State(items, self.__grammar)
        self.__transitions = []
        self.__build(self.__start, self.__transitions, {self.__start})

    @property
    def transitions(self) -> List[StateTableElement]:
        return self.__transitions

    def __build(self, current_state: State, transitions: dict, visited_states):
        for symbol in (item.next for item in current_state.items if item.has_next):
            next_state = current_state.go_to(symbol)
            if next_state in visited_states:
                transitions.append(StateTableElement(current_state, next_state, symbol))
                continue
            visited_states.add(next_state)
            if next_state.is_valid:
                transitions.append(StateTableElement(current_state, next_state, symbol))
                self.__build(next_state, transitions, visited_states)
