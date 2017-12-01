from parsing.domain.symbol import Symbol
from parsing.domain.symbol_type import SymbolType


class Terminal(Symbol):

    def __init__(self, value: str):
        super().__init__(value)

    @property
    def type(self):
        return SymbolType.TERMINAL
