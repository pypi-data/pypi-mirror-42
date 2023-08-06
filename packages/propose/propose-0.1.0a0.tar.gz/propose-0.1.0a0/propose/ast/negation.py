from .unary import Unary

class Negation(Unary):
    def __str__(self):
        return '¬' + str(self.formula)

    def to_string(self, formulas, offset = 0):
        formulas.update({offset: self})
        return '¬' + self.formula.to_string(formulas, offset + 1)

    def eval(self, binding):
        return not self.formula.eval(binding)
