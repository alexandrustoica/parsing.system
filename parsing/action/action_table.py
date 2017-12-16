from typing import List

from parsing.action.action import Action
from parsing.action.action_type import ActionType
from parsing.action.destination_state import DestinationState
from parsing.domain.state import State
from parsing.domain.state_finite_automaton import StateFiniteAutomaton


class ActionTable:

    def __init__(self, state_finite_automaton: StateFiniteAutomaton):
        self.__automaton = state_finite_automaton
        self.__actions = self.__build(state_finite_automaton.states, [])

    def __build(self, states: List[State], accumulator: List) -> List[Action]:
        if len(states) == 0:
            return accumulator
        return self.__build(states[1:], accumulator + [self.__get_action_for_state(states[0])])

    def __get_action_for_state(self, state: State) -> Action:
        return Action(state, ActionType.action_for_state(state), self.__get_destinations_for_state(state))

    def __get_destinations_for_state(self, state: State) -> List[DestinationState]:
        return [DestinationState(transition.destination, transition.symbol)
                for transition in self.__automaton.transitions if transition.source == state]

    def __str__(self):
        return "\n".join([str(action) for action in self.__actions])

    @property
    def actions(self) -> List[Action]:
        return self.__actions

    def get_index_for(self, state: State) -> int:
        return list(map(lambda action: action.source, self.__actions)).index(state)
