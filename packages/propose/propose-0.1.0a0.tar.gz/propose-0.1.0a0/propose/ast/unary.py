from .formula import Formula

class Unary(Formula):
    def __init__(self, formula: Formula):
        self.formula = formula
