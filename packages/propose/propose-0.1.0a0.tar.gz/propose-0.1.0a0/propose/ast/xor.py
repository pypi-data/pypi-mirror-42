from .binary import Binary

class Xor(Binary):
    def __str__(self):
        return '(' + str(self.left) + ' ⊕ ' + str(self.right) + ')'

    def to_string(self, formulas, offset = 0):
        left = self.left.to_string(formulas, offset + 1)
        formulas.update({(offset + 2 + len(left)): self})
        return '(' + left + ' ⊕ ' + self.right.to_string(formulas, offset + 4 + len(left)) + ')'

    def eval(self, binding):
        return (self.left.eval(binding) and not self.right.eval(binding)) or (not self.left.eval(binding) and self.right.eval(binding))
