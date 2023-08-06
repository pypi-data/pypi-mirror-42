from .formula import Formula

class Binary(Formula):
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right
