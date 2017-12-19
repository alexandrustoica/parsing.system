from parsing.domain.symbol import Symbol
from parsing.state.state import State


class StateTransition:

    def __init__(self, source: State, destination: State, symbol: Symbol):
        self.source = source
        self.destination = destination
        self.symbol = symbol

    def __str__(self):
        return "{} ====> {} with {}".format(repr(self.source), repr(self.destination), str(self.symbol))

    def __repr__(self):
        return str(self)
