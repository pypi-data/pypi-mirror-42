from .formula import Formula

class F(Formula):
    def __str__(self):
        return 'false'

    def to_string(self, formulas, offset = 0):
        return str(self)

    def eval(self, binding):
        return False
