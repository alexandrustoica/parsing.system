from enum import Enum


class ActionType(Enum):

    MOVEMENT = 0
    ACCEPT = 1
    RETURN = 2

    @classmethod
    def action_for_state(cls, state):
        return ActionType.ACCEPT if state.is_final() \
            else ActionType.RETURN if state.is_last() \
            else ActionType.MOVEMENT
