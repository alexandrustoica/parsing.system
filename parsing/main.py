from parsing.domain.context_free_grammar import ContextFreeGrammar
from parsing.domain.non_terminal import NonTerminal
from parsing.domain.rule import Rule
from parsing.domain.symbol import Symbol
from parsing.domain.terminal import Terminal


def main():
    non_terminals = [NonTerminal("S"), NonTerminal("A"), NonTerminal("B")]
    alphabet = [Terminal("a"), Terminal("b"), Terminal("c")]
    rule = Rule(NonTerminal("A"), [Symbol("a")])
    rules = [rule]
    start = NonTerminal("S")
    grammar = ContextFreeGrammar(non_terminals, alphabet, rules, start)
    print(grammar.extend())


main()
