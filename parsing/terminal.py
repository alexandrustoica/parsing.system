from parsing.symbol import Symbol


class Terminal(Symbol):

    def __init__(self, value: str):
        super().__init__(value)