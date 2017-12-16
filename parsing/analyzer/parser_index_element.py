from parsing.domain.symbol import Symbol


class ParserIndexElement:

    def __init__(self, index: int, symbol: Symbol):
        self.__symbol = symbol
        self.__index = index

    @property
    def symbol(self):
        return self.__symbol

    @property
    def index(self):
        return self.__index
