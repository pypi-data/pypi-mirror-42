from propose.ast.formula import Formula

def render_ast(formula, indentation: int = 0):
    result = ''

    if isinstance(formula, Formula):
        result += '(' + type(formula).__name__
        for key, value in formula.__dict__.items():
            if isinstance(value, Formula):
                result += ' ' + render_ast(value, indentation)
            elif isinstance(value, (list, dict)):
                result += render_ast(value, indentation)
        result += ')'

    return result

def _print_indented(value, indentation):
    return indentation * '  ' + value
