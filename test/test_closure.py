from unittest import TestCase
from parsing.domain.state_machine import StateMachine
from parsing.domain.state import State

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.parser.closure import Closure
from parsing.parser.item import ParserItem
from parsing.domain.rule import Rule
from parsing.domain.terminal import Terminal


class TestClosure(TestCase):

    def setUp(self):
        # TODO: Read Grammar From Json
        non_terminals = [NonTerminal("S"), NonTerminal("A")]
        alphabet = [Terminal("a"), Terminal("b"), Terminal("c")]
        rules = [Rule(NonTerminal("S"), [Terminal("a"), NonTerminal("A")]),
                 Rule(NonTerminal("A"), [Terminal("b"), NonTerminal("A")]),
                 Rule(NonTerminal("A"), [Terminal("c")])]
        start = NonTerminal("S")
        self.grammar = ContextFreeGrammar(non_terminals, alphabet, rules, start)

    def test_is_generating_closure(self):
        # TODO: Make better tests
        # declarations:
        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("S'"))[0])
        # when:
        items = Closure(item, extended).closure()
        # then:
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].left, NonTerminal("S'"))
        self.assertEqual(items[1].left, NonTerminal("S"))

        print(self.grammar)

    def test_is_going_to(self):
        # TODO: Make better tests
        # declarations:
        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("S'"))[0])
        items = Closure(item, extended).closure()
        state = State(items, self.grammar)
        # when
        actual = state.go_to(Terminal("a"))
        # then:
        self.assertEqual(len(actual.items), 3)
        self.assertEqual(actual.items[0].left, NonTerminal("S"))
        self.assertEqual(actual.items[1].left, NonTerminal("A"))
        self.assertEqual(actual.items[2].left, NonTerminal("A"))

    def test_state_machine(self):

        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("S'"))[0])
        items = Closure(item, extended).closure()
        state = State(items, self.grammar)
        machine = StateMachine(state)
        pass

test = TestClosure()
test.setUp()
test.test_state_machine()