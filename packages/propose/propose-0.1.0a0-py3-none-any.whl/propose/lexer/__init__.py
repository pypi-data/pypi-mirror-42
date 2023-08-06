from .lexer import Lexer

lexer = Lexer().get_lexer()

def lex(input):
    return lexer.lex(input)
