from unittest import TestCase
from parsing.domain.state_machine import StateMachine
from parsing.domain.state import State

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.domain.symbol import Symbol
from parsing.parser.closure import Closure
from parsing.parser.item import ParserItem


class TestClosure(TestCase):

    def setUp(self):
        grammar = {
            'terminals': ['a', 'b', 'c'],
            'non-terminals': ['S', 'A'],
            'rules': ['S -> aA', 'A -> bA', 'A -> c'],
            'start': 'S'
        }
        self.grammar = ContextFreeGrammar.from_dictionary(grammar)

    def test_is_generating_closure(self):
        # declarations:
        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("E"))[0])
        # when:
        items = Closure(item, extended).closure()
        # then:
        self.assertEqual(items, [ParserItem.from_string('E -> .S'),
                                 ParserItem.from_string('S -> .aA')])

        print(self.grammar)

    def test_is_going_to(self):
        # declarations:
        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("E"))[0])
        items = Closure(item, extended).closure()
        state = State(items, self.grammar)
        # when
        actual = state.go_to(Symbol("a"))
        # then:
        self.assertEqual(actual.items,
                         [ParserItem.from_string('S -> a.A'),
                          ParserItem.from_string('A -> .bA'),
                          ParserItem.from_string('A -> .c')])
