from unittest import TestCase

from parsing.action.action_table import ActionTable
from parsing.analyzer.flux_semantic_analyzer import FluxSemanticAnalyzer
from parsing.analyzer.internal_form import InternalForm
from parsing.analyzer.semantic_analyzer import SemanticAnalyzer
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
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("abbbc"))
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
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        action = analyzer.next_action
        # then:
        self.assertEqual(action.source, analyzer.next_state)

    def test_when_shifting_analyzer_expect_valid_next_parser_step(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("abbbc"))
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
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        next_parser_step = analyzer.shift().shift().shift().shift().shift().reduce().reduce().parser_step
        # then:
        self.assertEqual(next_parser_step.current_state.items, [ParserItem.from_string('A -> bA.')])

    def test_when_analyzer_accepts_input_expect_is_accepted_equals_true(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        actual = analyzer.shift().shift().shift().shift().shift().reduce().reduce().reduce().reduce().reduce().is_accepted
        # then:
        self.assertTrue(actual)

    def test_when_given_correct_expression_expect_analyzer_returns_true(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("abbbc"))
        # when:
        actual = analyzer.analyze()
        # print(actual)
        # then:
        self.assertTrue(actual)

    def test_when_complex_grammar_example_expect_analyzer_to_work(self):
        # given:
        # TODO Improve && Solve program -> .ε
        data = {
            'terminals': ['program', 'block', 'declarations', 'statements', 'declaration', 'type', 'identifier',
                          'expression', 'constant', 'statement', 'assignment', 'control_statement', 'io_statement',
                          'conditional_statement', 'loop_statement', 'condition', 'relation', 'sign_atom',
                          'operation', 'atom', 'low_level_operation', 'high_level_operation', 'range'],
            'non-terminals': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                              '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27'],
            'rules': [
                "program -> block",
                "block -> declarations",
                "block -> statements",
                "declarations -> ",
                "declarations -> declaration declarations",
                "declaration -> type identifier 4 expression 5",
                "declaration -> type identifier 5",
                "type -> 2",
                "type -> 3",
                "identifier -> 0",
                "constant -> 1",
                "constant -> 27 1 27",
                "statements -> ",
                "statements -> statement statements",
                "statement -> assignment",
                "statement -> control_statement",
                "statement -> io_statement",
                "assignment -> identifier 4 expression 5",
                "io_statement -> 6 10 11 5",
                "io_statement -> 7 10 identifier 11 5",
                "control_statement -> conditional_statement",
                "control_statement -> loop_statement",
                "conditional_statement -> 8 10 expression 11 12 block 13",
                # "conditional_statement -> conditional_statement 12 9 8 10 condition 11 12 block 13 13",
                # "conditional_statement -> conditional_statement 12 9 12 block 13 13",
                # "condition -> expression",
                # "condition -> expression relation expression",
                "expression -> sign_atom",
                "expression -> 10 expression 11",
                "expression -> expression operation atom",
                "sign_atom -> atom",
                "sign_atom -> 15 atom",
                "operation -> low_level_operation",
                "operation -> high_level_operation",
                "low_level_operation -> 14",
                "low_level_operation -> 15",
                "high_level_operation -> 16",
                "high_level_operation -> 17",
                "high_level_operation -> relation",
                "atom -> identifier",
                "atom -> constant",
                "relation -> 22",
                "relation -> 23",
                "relation -> 21",
                "relation -> 20",
                "relation -> 19",
                "relation -> 18",
                "loop_statement -> 24 10 type identifier 26 range 11 12 block 13",
                "range -> identifier",
                "range -> 25 10 constant 26 constant 11"],
            'start': 'program'
        }
        grammar = ContextFreeGrammar.from_complex_dictionary(data)
        internal_form = InternalForm('../pif.txt')
        analyzer = FluxSemanticAnalyzer(internal_form, grammar)
        # when:
        actual = analyzer.analyze()
        # then:
        self.assertTrue(actual)

    def test_when_given_wrong_expression_expect_analyzer_raises_exception(self):
        # given:
        action_table = ActionTable(StateFiniteAutomaton(self.grammar))
        analyzer = SemanticAnalyzer(action_table, Symbol.from_string("aabc"))
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

    def test_when_grammar_has_empty_rule_expect_to_accept_input_stream(self):
        # given:
        data = {
            'terminals': ['1', '2'],
            'non-terminals': ['S'],
            'rules': ['S -> ', 'S -> 1 S'],
            'start': 'S'
        }
        grammar = ContextFreeGrammar.from_complex_dictionary(data)
        # when/then:
        action_table = ActionTable(StateFiniteAutomaton(grammar))
        analyzer = SemanticAnalyzer(action_table, Symbol.from_complex_string("1 1 1"))
        # when:
        actual = analyzer.analyze()
        # then:
        self.assertTrue(actual)

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
