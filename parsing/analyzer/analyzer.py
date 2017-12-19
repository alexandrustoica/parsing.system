from typing import List

from parsing.action.action_table import ActionTable
from parsing.analyzer.parser_step import ParserStep
from parsing.domain.symbol import Symbol
from parsing.state.destination_state import DestinationState


class Analyzer:

    def __init__(self, action_table: ActionTable, input_stream: List[Symbol], parser_step: ParserStep = None):
        self.__action_table = action_table
        self.__parser_step = parser_step if parser_step is not None \
            else self.__build_initial_parser_step(input_stream)

    def __build_initial_parser_step(self, input_stream: List[Symbol]):
        return ParserStep([DestinationState(self.__action_table.actions[0].source, Symbol("$"))], input_stream, [])

    @property
    def action_table(self) -> ActionTable:
        return self.__action_table

    @property
    def parser_step(self) -> ParserStep:
        return self.__parser_step

    @property
    def next_state(self) -> DestinationState:
        return self.__action_table.next_state(self.__parser_step.current_state, self.__parser_step.current_symbol)

    def shift(self):
        return Analyzer(self.__action_table, None, self.__parser_step.shift(self.next_state))

    def reduce(self):
        return Analyzer(self.__action_table, None,
                        self.__parser_step.reduce(self.__parser_step.last_state_from_stack, self.__action_table))

    def next_action(self):
        return self.__action_table.get_action_for_state(self.next_state)
