from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self.build = None

    def _add_tokens(self):
        self.lexer.add('->', r'\-\>')
        self.lexer.add('<->', r'\<\-\>')
        self.lexer.add('+', r'\+')
        self.lexer.add('*', r'\*')
        self.lexer.add('!', r'\!')
        self.lexer.add('(', r'\(')
        self.lexer.add(')', r'\)')
        self.lexer.add('false', r'false')
        self.lexer.add('true', r'true')
        self.lexer.add('xor', r'xor')
        self.lexer.add('LITERAL', r'[A-Za-z]+')

        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self._add_tokens()
        self.build = self.lexer.build()
        return self

    def lex(self, input):
        if self.build is None:
            self.get_lexer()

        return self.build.lex(input)
