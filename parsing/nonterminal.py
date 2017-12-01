from parsing.symbol import Symbol


class NonTerminal(Symbol):

    def __init__(self, value: str):
        super().__init__(value)