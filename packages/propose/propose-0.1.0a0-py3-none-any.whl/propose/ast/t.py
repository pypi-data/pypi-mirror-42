from .formula import Formula

class T(Formula):
    def __str__(self):
        return 'true'

    def to_string(self, formulas, offset = 0):
        return str(self)

    def eval(self, binding):
        return True
