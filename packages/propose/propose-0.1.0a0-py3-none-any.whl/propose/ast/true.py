from .formula import Formula

class True(Formula):
    def __str__(self):
        return '<True>'

    def eval(self, binding):
        return True
