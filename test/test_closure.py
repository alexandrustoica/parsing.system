from unittest import TestCase

from parsing.action.action_table import ActionTable
from parsing.action.action_type import ActionType
from parsing.domain.rule import Rule
from parsing.domain.state_finite_automaton import StateFiniteAutomaton
from parsing.domain.state import State, IncompatibleStateToRuleException

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

    def test_state_machine(self):
        # when:
        transitions = StateFiniteAutomaton(self.grammar).transitions
        # then:
        self.assertEqual(len(transitions), 8)
        self.assertEqual((transitions[0].source.items,
                          transitions[0].destination.items,
                          transitions[0].symbol),
                         ([ParserItem.from_string('E -> .S'),
                           ParserItem.from_string('S -> .aA')],
                          [ParserItem.from_string('E -> S.')],
                          NonTerminal("S")))

    def test_when_item_parser_represents_rule_expect_item_parser_equal_to_rule(self):
        # give:
        item = ParserItem.from_string("E -> S.")
        # when/then:
        self.assertTrue(item.equals_rule(Rule.from_string("E -> S")))

    def test_when_item_parser_not_represents_rule_expect_item_parser_not_equal_to_rule(self):
        # give:
        item = ParserItem.from_string("E -> S.")
        # when/then:
        self.assertFalse(item.equals_rule(Rule.from_string("S -> aA")))

    def test_when_state_is_last_and_represents_rule_expect_true(self):
        # give:
        transitions = StateFiniteAutomaton(self.grammar).transitions
        last_state = transitions[7].destination
        non_last_state = transitions[1].destination
        # when/then:
        self.assertTrue(last_state.is_last() and not non_last_state.is_last())

    def test_when_state_is_final_and_represents_rule_expect_true(self):
        # give:
        transitions = StateFiniteAutomaton(self.grammar).transitions
        final_state = transitions[0].destination
        non_final_state = transitions[1].destination
        # when/then:
        self.assertTrue(final_state.is_final() and not non_final_state.is_final())

    def test_when_state_converted_to_rule_and_state_represents_rule_expect_rule(self):
        # give:
        final_state = StateFiniteAutomaton(self.grammar).transitions[0].destination
        # when/then:
        self.assertEqual(final_state.to_rule(), Rule.from_string("E -> S"))

    def test_when_state_converted_to_rule_and_state_not_represents_rule_expect_exception(self):
        # give:
        state = StateFiniteAutomaton(self.grammar).transitions[1].destination
        # when/then:
        self.assertRaises(IncompatibleStateToRuleException, state.to_rule)

    def test_when_building_action_table_from_grammar_expect_valid_action_table(self):
        # given:
        state_finite_automaton = StateFiniteAutomaton(self.grammar)
        # when:
        action_table = ActionTable(state_finite_automaton)
        print(action_table)
        # then:
        self.assertTrue(len(action_table.actions), len(state_finite_automaton.states))

if __name__ == "__main__":
    test = TestClosure()

    test.setUp()
    test.test_is_generating_closure()
    test.test_is_going_to()
    test.test_state_machine()
