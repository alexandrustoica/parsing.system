from parsing.domain.symbol import Symbol
from parsing.state.state import State


class DestinationState(State):

    def __init__(self, state: State, symbol: Symbol):
        State.__init__(self, state._parse_items, state._grammar)
        self.__symbol = symbol

    @property
    def symbol(self):
        return self.__symbol

    def __str__(self):
        return "({}, {})".format(self.__symbol, repr(self))