from typing import List

from parsing.action.action_table import ActionTable
from parsing.action.action_type import ActionType
from parsing.analyzer.parser_atom import ParserAtom
from parsing.analyzer.parser_index_element import ParserIndexElement
from parsing.domain.symbol import Symbol


class Analyzer:

    def __init__(self, action_table: ActionTable, data: List[Symbol]):
        self.__action_table = action_table
        self.__parser_atom = ParserAtom([ParserIndexElement(0, Symbol("$"))], data, [])

    @property
    def action_table(self):
        return self.__action_table

    def __get_action_type_for_current_index(self):
        return self.__get_action_type_for_index(self.__parser_atom.current.index)

    def __get_action_type_for_index(self, index) -> ActionType:
        return self.__action_table.actions[index].action_type
