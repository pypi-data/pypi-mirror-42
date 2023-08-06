from .formula import Formula

class False(Formula):
    def __str__(self):
        return '<False>'

    def eval(self, binding):
        return False
