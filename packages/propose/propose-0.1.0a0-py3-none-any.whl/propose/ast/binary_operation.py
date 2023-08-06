from .expression import Expression

class BinaryOperation(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
