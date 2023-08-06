from .formula import Formula

class Literal(Formula):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)

    def to_string(self, formulas, offset = 0):
        return str(self)

    def eval(self, binding):
        return binding[self.name]
