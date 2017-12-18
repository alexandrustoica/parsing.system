from typing import List
from parsing.action.action_type import ActionType
from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.action.action_table import ActionTable

from parsing.analyzer.parser_index_element import ParserIndexElement
from parsing.domain.symbol import Symbol


class ParserAtom:

    def __init__(self, route: List[ParserIndexElement],
                 symbols: List[Symbol],
                 success_route: List[int],
                 action_table: ActionTable,
                 grammar: ContextFreeGrammar):
        self.__route = route
        self.__symbols = symbols
        self.__success_route = success_route
        self.__action_table = action_table
        self.__grammar = grammar
        self.__cursor = 0

    def move(self):
        action = self.__action_table.actions[self.__cursor]
        act_type = action.action_type
        if act_type == ActionType.MOVEMENT:
            ans = ParserAtom(self.route + [ParserIndexElement(self.__cursor, self.first_symbol)],
                          self.symbols[1:],
                          self.success_route)
        elif act_type == ActionType.RETURN:
            pass
        elif act_type == ActionType.ACCEPT:
            pass

        # TODO: Move cursor

        

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
