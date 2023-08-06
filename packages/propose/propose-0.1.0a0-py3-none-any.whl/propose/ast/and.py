from .binary_operation import BinaryOperation

class And(BinaryOperation):
    def __str__(self):
        return '<And left=' + str(self.left) + ', right=' + str(self.right) + '>'
