from typing import List


from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.parser.closure import Closure
from parsing.parser.item import ParserItem
from parsing.state.state import State
from parsing.state.state_transition import StateTransition


class StateFiniteAutomaton:

    def __init__(self, grammar: ContextFreeGrammar):
        self.__grammar = grammar
        extended = self.__grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("E"))[0])
        items = Closure(item, extended).closure()
        self.__start = State(items, self.__grammar)
        self.__transitions = []
        self.__states = [self.__start]
        self.__build(self.__start, self.__transitions, self.__states)

    @property
    def transitions(self) -> List[StateTransition]:
        return self.__transitions

    @property
    def states(self) -> List[State]:
        return self.__states

    def __build(self, current_state: State,
                transitions: List[StateTransition],
                visited_states: List[State]):
        for symbol in (item.next for item in current_state.items if item.has_next):
            next_state = current_state.go_to(symbol)
            if next_state in visited_states:
                transitions.append(StateTransition(current_state, next_state, symbol))
                continue
            visited_states.append(next_state)
            if next_state.is_valid:
                transitions.append(StateTransition(current_state, next_state, symbol))
                self.__build(next_state, transitions, visited_states)
