from typing import List

from parsing.action.action import Action
from parsing.action.action_type import ActionType
from parsing.analyzer.analyzer_conflict import AnalyzerConflict
from parsing.domain.symbol import Symbol
from parsing.state.destination_state import DestinationState
from parsing.state.state import State
from parsing.state.state_finite_automaton import StateFiniteAutomaton


def validated_result(foo):
    def wrapper(*args, **kwargs):
        result = foo(*args, **kwargs)
        if result is None:
            raise AnalyzerConflict(args)
        return result
    return wrapper


class ActionTable:
    def __init__(self, state_finite_automaton: StateFiniteAutomaton):
        self.__automaton = state_finite_automaton
        self.__actions = self.__build(state_finite_automaton.states, [])

    @property
    def actions(self) -> List[Action]:
        return self.__actions

    @validated_result
    def next_state(self, current_state: State, symbol: Symbol) -> DestinationState:
        symbol = 'ε' if symbol is None else symbol
        return next(filter(lambda destination: destination.symbol == symbol,
                           next(filter(lambda action: action.source == current_state,
                                       self.actions), None).destinations), None)

    @validated_result
    def get_action_for_state(self, state: State) -> Action:
        return next(filter(lambda action: action.source == state, self.actions), None)

    def __build(self, states: List[State], accumulator: List) -> List[Action]:
        if len(states) == 0:
            return accumulator
        return self.__build(states[1:], accumulator + [self.__create_action_for_state(states[0])])

    def __create_action_for_state(self, state: State) -> Action:
        return Action(state, ActionType.action_for_state(state), self.__create_destinations_for_state(state))

    def __create_destinations_for_state(self, state: State) -> List[DestinationState]:
        return [DestinationState(transition.destination, transition.symbol)
                for transition in self.__automaton.transitions if transition.source == state]

    def __str__(self):
        return "\n".join([str(action) for action in self.__actions])
