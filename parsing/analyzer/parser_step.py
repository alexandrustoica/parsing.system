from typing import List

from parsing.domain.symbol import Symbol
from parsing.state.destination_state import DestinationState
from parsing.state.state import State


class ParserStep:
    def __init__(self, stack: List[DestinationState],
                 input_stream: List[Symbol],
                 output_stream: List[State]):
        self.__stack = stack
        self.__input_stream = input_stream
        self.__output_stream = output_stream

    def shift(self, state: DestinationState):
        return ParserStep(self.__stack + [state],
                          self.__input_stream[1:],
                          self.__output_stream)

    @property
    def current_state(self):
        return self.__stack[-1]

    @property
    def current_symbol(self):
        return self.__input_stream[0]

    def __str__(self):
        return "[{}, {}$, {}]".format(''.join(str(element) for element in self.__stack),
                                      ''.join(str(symbol) for symbol in self.__input_stream),
                                      str(self.__output_stream))

    def __repr__(self):
        return str(self)


