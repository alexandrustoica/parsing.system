from parsing.contextfreegrammer import ContextFreeGrammar
from parsing.nonterminal import NonTerminal
from parsing.rule import Rule
from parsing.symbol import Symbol
from parsing.terminal import Terminal


def main():
    non_terminals = [NonTerminal("S"), NonTerminal("A"), NonTerminal("B")]
    alphabet = [Terminal("a"), Terminal("b"), Terminal("c")]
    rule = Rule(NonTerminal("A"), [Symbol("a")])
    rules = [rule]
    start = NonTerminal("S")
    grammar = ContextFreeGrammar(non_terminals, alphabet, rules, start)
    print(grammar)


main()
