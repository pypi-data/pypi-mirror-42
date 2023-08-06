import decimal

from rply import ParserGenerator

from propose.ast import *

class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            ['->', '<->', '+', '*', '!', '(', ')', 'false', 'true', 'xor', 'LITERAL'],
            precedence=[
                ('left', ['<->']),
                ('left', ['->']),
                ('left', ['xor']),
                ('left', ['+']),
                ('left', ['*']),
                ('left', ['!'])
            ]
        )

    def _add_productions(self):
        @self.pg.production('formula : binary')
        @self.pg.production('formula : unary')
        @self.pg.production('formula : grouped')
        @self.pg.production('formula : literal')
        def formula(state, p):
            return p[0]

        @self.pg.production('literal : false')
        @self.pg.production('literal : true')
        @self.pg.production('literal : LITERAL')
        def literal(state, p):
            if p[0].gettokentype() == 'false':
                return F()
            elif p[0].gettokentype() == 'true':
                return T()
            else:
                if p[0].getstr() not in state.literals:
                    state.literals.append(p[0].getstr())
                return Literal(name=p[0].getstr())

        @self.pg.production('grouped : ( formula )')
        def grouped(state, p):
            return p[1]

        @self.pg.production('unary : ! formula')
        def unary(state, p):
            return Negation(formula=p[1])

        @self.pg.production('binary : formula <-> formula')
        @self.pg.production('binary : formula -> formula')
        @self.pg.production('binary : formula xor formula')
        @self.pg.production('binary : formula + formula')
        @self.pg.production('binary : formula * formula')
        def binary(state, p):
            if p[1].gettokentype() == '<->':
                return Biconditional(left=p[0], right=p[2])
            elif p[1].gettokentype() == '->':
                return Implication(left=p[0], right=p[2])
            elif p[1].gettokentype() == 'xor':
                return Xor(left=p[0], right=p[2])
            elif p[1].gettokentype() == '+':
                return Or(left=p[0], right=p[2])
            elif p[1].gettokentype() == '*':
                return And(left=p[0], right=p[2])

    def get_parser(self):
        self._add_productions()
        return self.pg.build()
