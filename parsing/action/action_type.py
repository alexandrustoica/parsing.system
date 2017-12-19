from enum import Enum


class ActionType(Enum):

    SHIFT = 0
    ACCEPT = 1
    REDUCE = 2

    @classmethod
    def action_for_state(cls, state):
        return ActionType.ACCEPT if state.is_final() \
            else ActionType.REDUCE if state.is_last() \
            else ActionType.SHIFT
