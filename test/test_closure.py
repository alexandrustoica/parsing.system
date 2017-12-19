from unittest import TestCase


from parsing.action.action_table import ActionTable
from parsing.analyzer.analyzer import Analyzer
from parsing.analyzer.analyzer_conflict import AnalyzerConflict
from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.domain.rule import Rule
from parsing.domain.symbol import Symbol
from parsing.parser.closure import Closure
from parsing.parser.parser_item import ParserItem
from parsing.state.incompatible_state_to_rule import IncompatibleStateToRuleException
from parsing.state.state import State
from parsing.state.state_conflict import StateConflict
from parsing.state.state_finite_automaton import StateFiniteAutomaton


class TestAnalyzer(TestCase):

    def setUp(self):
        grammar = {
            'terminals': ['a', 'b', 'c'],
            'non-terminals': ['S', 'A'],
            'rules': ['S -> aA', 'A -> bA', 'A -> c'],
            'start': 'S'
        }
        self.grammar = ContextFreeGrammar.from_dictionary(grammar)

    def test_when_generating_closure_expect_valid_items(self):
        # declarations:
        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("E"))[0])
        # when:
        items = Closure(item, extended).closure()
        # then:
        self.assertEqual(items, [ParserItem.from_string('E -> . S'),
                                 ParserItem.from_string('S -> . a A')])

    def test_when_is_going_to_next_state_expect_valid_next_state(self):
        # declarations:
        extended = self.grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("E"))[0])
        items = Closure(item, extended).closure()
        state = State(items, self.grammar)
        # when
        actual = state.go_to(Symbol("a"))
        # then:
        self.assertEqual(actual.items,
                         [ParserItem.from_string('S -> a . A'),
                          ParserItem.from_string('A -> . b A'),
                          ParserItem.from_string('A -> . c')])

    def test_when_generating_state_finite_automaton_expect_valid_transitions(self):
        # when:
        transitions = StateFiniteAutomaton(self.grammar).transitions
        # then:
        self.assertEqual(len(transitions), 8)
        self.assertEqual((transitions[0].source.items,
                          transitions[0].destination.items,
                          transitions[0].symbol),
                         ([ParserItem.from_string('E -> . S'),
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
        self.assertFalse(item.equals_rule(Rule.from_string("S -> a A")))

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
        # then:
        self.assertTrue(len(action_table.actions), len(state_finite_automaton.states))

    def test_when_getting_next_state_from_parser_step_expect_next_state(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        next_state = analyzer.next_state
        # then:
        self.assertEqual(next_state.items,
                         [ParserItem.from_string('S -> a.A'),
                          ParserItem.from_string('A -> .bA'),
                          ParserItem.from_string('A -> .c')])

    def test_when_getting_action_for_next_state_expect_right_action(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        action = analyzer.next_action
        # then:
        self.assertEqual(action.source, analyzer.next_state)

    def test_when_shifting_analyzer_expect_valid_next_parser_step(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        next_parser_step = analyzer.shift().parser_step

        # then:
        self.assertEqual(next_parser_step.current_state.items,
                         [ParserItem.from_string('S -> a.A'),
                          ParserItem.from_string('A -> .bA'),
                          ParserItem.from_string('A -> .c')])

    def test_when_reducing_analyzer_expect_valid_next_parser_step(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        next_parser_step = analyzer.shift().shift().shift().shift().shift().reduce().reduce().parser_step
        # then:
        self.assertEqual(next_parser_step.current_state.items, [ParserItem.from_string('A -> bA.')])

    def test_when_analyzer_accepts_input_expect_is_accepted_equals_true(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        actual = analyzer.shift().shift().shift().shift().shift().reduce().reduce().reduce().reduce().reduce().is_accepted
        # then:
        self.assertTrue(actual)

    def test_when_given_correct_expression_expect_analyzer_returns_true(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        actual = analyzer.analyze()
        # print(actual)
        # then:
        self.assertTrue(actual)

    def test_when_complex_grammar_example_expect_analyzer_to_work(self):
        # given:
        data = {
            'terminals': ['ana', 'banana', 'cot'],
            'non-terminals': ['start', 'next'],
            'rules': ['start -> ana next', 'next -> banana next', 'next -> cot'],
            'start': 'start'
        }
        grammar = ContextFreeGrammar.from_complex_dictionary(data)
        action_table = ActionTable(StateFiniteAutomaton(grammar))
        analyzer = Analyzer(action_table, Symbol.from_complex_string("ana banana banana banana cot"))
        # when:
        actual = analyzer.analyze()
        # then:
        self.assertTrue(actual)

    def test_when_given_wrong_expression_expect_analyzer_raises_exception(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = Analyzer(action_table, Symbol.from_string("aabc"))
        # when/then:
        self.assertRaises(AnalyzerConflict, analyzer.analyze)

    def test_when_state_in_reduce_reduce_conflict_expect_state_conflict(self):
        # given:
        data = {
            'terminals': ['1', '2'],
            'non-terminals': ['S', 'A', 'B'],
            'rules': ['A -> 1', 'B -> 1', 'S -> A1', 'S -> B2'],
            'start': 'S'
        }
        grammar = ContextFreeGrammar.from_dictionary(data)
        # when/then:
        self.assertRaises(StateConflict, StateFiniteAutomaton, grammar)

    def test_when_state_in_shift_reduce_conflict_expect_state_conflict(self):
        # given:
        data = {
            'terminals': ['1'],
            'non-terminals': ['S'],
            'rules': ['S -> 1', 'S -> 1S'],
            'start': 'S'
        }
        grammar = ContextFreeGrammar.from_dictionary(data)
        # when/then:
        self.assertRaises(StateConflict, StateFiniteAutomaton, grammar)


if __name__ == "__main__":
    test = TestAnalyzer()

    test.setUp()
    test.test_when_generating_closure_expect_valid_items()
    test.test_whne_is_going_to_next_state_expect_valid_next_state()
    test.test_when_generating_state_finite_automaton_expect_valid_transitions()
