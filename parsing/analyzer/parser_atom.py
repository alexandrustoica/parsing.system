from typing import List

from parsing.analyzer.parser_index_element import ParserIndexElement
from parsing.domain.symbol import Symbol


class ParserAtom:

    def __init__(self, route: List[ParserIndexElement],
                 symbols: List[Symbol],
                 success_route: List[int]):
        self.__route = route
        self.__symbols = symbols
        self.__success_route = success_route

    def move(self, index: int):
        return ParserAtom(self.route + [ParserIndexElement(index, self.first_symbol)],
                          self.symbols[-1:],
                          self.success_route)

    @property
    def route(self):
        return self.__route

    @property
    def symbols(self):
        return self.__symbols

    @property
    def success_route(self):
        return self.__success_route

    @property
    def current(self) -> ParserIndexElement:
        return self.__route[-1]

    @property
    def first_symbol(self) -> Symbol:
        return self.symbols[0]
