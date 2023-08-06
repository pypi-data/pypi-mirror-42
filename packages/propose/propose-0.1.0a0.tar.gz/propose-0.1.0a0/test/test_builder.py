from textwrap import dedent

from propose.builder import build
from propose.lexer import lex
from propose.parser import State, parse

def _build(input):
    tokens = lex(input)
    state = State()
    ast = parse(input, tokens, state)

    return build(state, ast, highlight=False)

def _match_output(expected, actual, msg):
    assert dedent(expected)[1:-1] == actual, msg

def test_and():
    input = """
            a * b
            """
    output = """
             a b | (a ∧ b)
             0 0 |    0
             0 1 |    0
             1 0 |    0
             1 1 |    1
             """

    _match_output(output, _build(dedent(input)), 'And')

def test_or():
    input = """
            a + b
            """
    output = """
             a b | (a ∨ b)
             0 0 |    0
             0 1 |    1
             1 0 |    1
             1 1 |    1
             """

    _match_output(output, _build(dedent(input)), 'Or')

def test_xor():
    input = """
            a xor b
            """
    output = """
             a b | (a ⊕ b)
             0 0 |    0
             0 1 |    1
             1 0 |    1
             1 1 |    0
             """

    _match_output(output, _build(dedent(input)), 'Xor')

def test_implication():
    input = """
            a -> b
            """
    output = """
             a b | (a → b)
             0 0 |    1
             0 1 |    1
             1 0 |    0
             1 1 |    1
             """

    _match_output(output, _build(dedent(input)), 'Implication')

def test_biconditional():
    input = """
            a <-> b
            """
    output = """
             a b | (a ↔ b)
             0 0 |    1
             0 1 |    0
             1 0 |    0
             1 1 |    1
             """

    _match_output(output, _build(dedent(input)), 'Biconditional')
