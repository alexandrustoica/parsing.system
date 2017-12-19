from typing import List

from parsing.action.action_table import ActionTable
from parsing.domain.symbol import Symbol
from parsing.state.destination_state import DestinationState


class ParserStep:

    def __init__(self, stack: List[DestinationState],
                 input_stream: List[Symbol],
                 output_stream: List[DestinationState]):
        self.__stack = stack
        self.__input_stream = input_stream
        self.__output_stream = output_stream

    def shift(self, state: DestinationState):
        return ParserStep(self.__stack + [state],
                          self.__input_stream[1:],
                          self.__output_stream)

    def reduce(self, state: DestinationState, action_table: ActionTable):
        return ParserStep(self.__replace_stack(state, action_table),
                          self.__input_stream,
                          [state] + self.__output_stream) if self.is_able_to_reduce(state) else None

    def __replace_stack(self, state: DestinationState, action_table: ActionTable) -> List[DestinationState]:
        return self.__remove_from_stack(state) + [action_table.next_state(self.__remove_from_stack(state)[-1], state.to_rule().left)]

    def __remove_from_stack(self, state: DestinationState) -> List[DestinationState]:
        return self.__stack[:-(len(state.to_rule().right))]

    def is_able_to_reduce(self, state: DestinationState):
        return self.__is_able_to_reduce(self.__stack[:], state.to_rule().right[:])

    def __is_able_to_reduce(self, stack: List[DestinationState], symbols_to_check: List[Symbol]) -> bool:
        return True if symbols_to_check == [] else self.__is_able_to_reduce(stack[:-1], symbols_to_check[:-1]) \
            if stack[-1].symbol == symbols_to_check[-1] else False

    @property
    def last_state_from_stack(self) -> DestinationState:
        return self.__stack[-1]

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





