from enum import Enum


class ActionType(Enum):

    MOVEMENT = 0
    ACCEPT = 1
    RETURN = 2

    def __init__(self, value):
        self._value = value

    @property
    def value(self) -> int:
        return self._value
