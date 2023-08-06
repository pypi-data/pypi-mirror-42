from .expression import Expression

class UnaryOperation(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression
