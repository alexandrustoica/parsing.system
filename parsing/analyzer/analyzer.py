from typing import List

from parsing.action.action import Action
from parsing.action.action_table import ActionTable
from parsing.analyzer.parser_atom import ParserAtom
from parsing.analyzer.parser_index_element import ParserIndexElement
from parsing.domain.state import State
from parsing.domain.symbol import Symbol


class Analyzer:

    def __init__(self, action_table: ActionTable, data: List[Symbol]):
        self.__action_table = action_table
        self.__parser_atom = ParserAtom([ParserIndexElement(0, Symbol("$"))], data, [])

    @property
    def action_table(self):
        return self.__action_table

    def apply_movement(self):
        self.__parser_atom = self.__parser_atom.move(self.__get_current_index())

    def __get_current_index(self) -> int:
        return self.action_table.get_index_for(self.__get_current_state())

    def __get_current_action(self) -> Action:
        return self.__action_table.actions[self.__parser_atom.current.index]

    def __get_current_state(self) -> State:
        return self.__get_current_action().source

    def __get_current_action_type(self):
        return self.__get_current_action().action_type

