from typing import List

from parsing.action.action_table import ActionTable
from parsing.analyzer.internal_form import InternalForm
from parsing.analyzer.semantic_analyzer import SemanticAnalyzer
from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.symbol import Symbol
from parsing.state.state_finite_automaton import StateFiniteAutomaton


class FluxSemanticAnalyzer:

    def __init__(self, internal_form: InternalForm, grammar: ContextFreeGrammar):
        self.__grammar = grammar
        self.__action_table = ActionTable(StateFiniteAutomaton(self.__grammar))
        self.__input_stream = self.__convert_internal_form_to_symbols(internal_form)
        self.__analyzer = SemanticAnalyzer(self.__action_table, self.__input_stream)

    def analyze(self):
        return self.__analyzer.analyze()

    @property
    def input_stream(self):
        return self.__input_stream

    @staticmethod
    def __convert_internal_form_to_symbols(internal_form: InternalForm) -> List[Symbol]:
        return [Symbol(item.key) for item in internal_form.atoms]
