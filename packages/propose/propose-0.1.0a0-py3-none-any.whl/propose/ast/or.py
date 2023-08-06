from .binary_operation import BinaryOperation

class Or(BinaryOperation):
    def __str__(self):
        return '<Or left=' + str(self.left) + ', right=' + str(self.right) + '>'
