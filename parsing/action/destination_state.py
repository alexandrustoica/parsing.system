from parsing.domain.state import State
from parsing.domain.symbol import Symbol


class DestinationState(State):

    def __init__(self, state: State, symbol: Symbol):
        State.__init__(self, state._parse_items, state._grammar)
        self.__symbol = symbol

    @property
    def symbol(self):
        return self.__symbol
