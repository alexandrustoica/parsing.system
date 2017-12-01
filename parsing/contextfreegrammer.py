from typing import List

from parsing.nonterminal import NonTerminal
from parsing.terminal import Terminal
from parsing.rule import Rule


class ContextFreeGrammar:

    def __init__(self, non_terminals: List[NonTerminal],
                 alphabet: List[Terminal],
                 rules: List[Rule],
                 start: NonTerminal):
        self.non_terminals = non_terminals
        self.alphabet = alphabet
        self.rules = rules
        self.start = start

    def __str__(self):
        return "NonTerminals: {}\nAlphabet: {}\nRules: {}\nStart: {}"\
            .format("".join(str(non_terminal) + " " for non_terminal in self.non_terminals),
                    "".join(str(terminal) + " " for terminal in self.alphabet),
                    "".join("\n\t{}".format(str(rule)) for rule in self.rules),
                    "" + str(self.start))