import json
import sys

from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.domain.rule import Rule
from parsing.domain.symbol import Symbol
from parsing.domain.terminal import Terminal

if __name__ == '__main__':
    with open(sys.argv[1], "r") as file:
        given = json.loads(file.read())
        non_terminals = [NonTerminal(x) for x in given["non_terminals"]]
        alphabet = [Terminal(x) for x in given["alphabet"]]
        rules = [Rule(NonTerminal(x), [Symbol(y)])
                 for x, y in [tuple(rule.split(" -> "))
                              for rule in given["rules"]]]
        start = NonTerminal(given["start"])
        grammar = ContextFreeGrammar(non_terminals, alphabet, rules, start)
        print(grammar.extend())
