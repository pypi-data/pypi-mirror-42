from .binary import Binary

class Implication(Binary):
    def __str__(self):
        return '(' + str(self.left) + ' → ' + str(self.right) + ')'

    def to_string(self, formulas, offset = 0):
        left = self.left.to_string(formulas, offset + 1)
        formulas.update({(offset + 2 + len(left)): self})
        return '(' + left + ' → ' + self.right.to_string(formulas, offset + 4 + len(left)) + ')'

    def eval(self, binding):
        return not self.left.eval(binding) or self.right.eval(binding)
