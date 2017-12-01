from unittest import TestCase

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.parser.closure import Closure
from parsing.parser.item import ParserItem
from parsing.domain.rule import Rule
from parsing.domain.terminal import Terminal


class TestClosure(TestCase):

    def test_is_generating_closure(self):
        # declarations:
        non_terminals = [NonTerminal("S"), NonTerminal("A")]
        alphabet = [Terminal("a"), Terminal("b"), Terminal("c")]
        rules = [Rule(NonTerminal("S"), [Terminal("a"), NonTerminal("A")]),
                 Rule(NonTerminal("A"), [Terminal("b"), NonTerminal("A")]),
                 Rule(NonTerminal("A"), [Terminal("c")])]
        start = NonTerminal("S")
        grammar = ContextFreeGrammar(non_terminals, alphabet, rules, start)
        extended = grammar.extend()
        item = ParserItem.item_for(extended.rules_of(NonTerminal("S'"))[0])
        # when:
        items = Closure(item, extended).closure
        # then:
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].left, NonTerminal("S'"))
        self.assertEqual(items[1].left, NonTerminal("S"))
