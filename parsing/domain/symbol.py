from _ast import List

from parsing.domain.symbol_type import SymbolType


class Symbol:

    def __init__(self, value: str):
        self._value = value

    @property
    def type(self):
        return SymbolType.SYMBOL

    @property
    def value(self):
        return self._value

    @classmethod
    def from_string(cls, string: str) -> List:
        return [Symbol(value) for value in string]

    def __eq__(self, other):
        return other.value == self._value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self._value

    def __hash__(self):
        return self._value.__hash__()