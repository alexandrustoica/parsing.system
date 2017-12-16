from typing import List

from parsing.action.action_type import ActionType
from parsing.action.destination_state import DestinationState
from parsing.domain.state import State


class Action:

    def __init__(self, source_state: State,
                 action_type: ActionType,
                 destination_states: List[DestinationState] = []):
        self._source_state = source_state
        self._action_type = action_type
        self._destination_states = destination_states

    def __str__(self):
        return "{} type: {} destinations: {}"\
            .format(str(self._source_state), str(self._action_type),
                    ", ".join([str(destination) for destination in self._destination_states]))

    @property
    def action_type(self) -> ActionType:
        return self._action_type
