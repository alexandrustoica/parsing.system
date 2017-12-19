from typing import List

from parsing.action.action_type import ActionType
from parsing.state.destination_state import DestinationState
from parsing.state.state import State


class Action:

    def __init__(self, source_state: State,
                 action_type: ActionType,
                 destination_states: List[DestinationState] = []):
        self._source_state = source_state
        self._action_type = action_type
        self._destination_states = destination_states

    def __str__(self):
        return "{} type: {} destinations: {}"\
            .format(repr(self._source_state), str(self._action_type),
                    ", ".join([str(destination) for destination in self._destination_states]))

    @property
    def action_type(self) -> ActionType:
        return self._action_type

    @property
    def source(self) -> State:
        return self._source_state

    @property
    def destinations(self) -> List[DestinationState]:
        return self._destination_states

    @property
    def get_state_based_on_symbol(self, symbol) -> State:
        return next(filter(lambda destination: destination.symbol == symbol, self.destinations), None)
