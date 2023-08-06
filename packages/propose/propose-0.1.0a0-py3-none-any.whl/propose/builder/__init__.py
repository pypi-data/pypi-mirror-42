import itertools

from colorama import Fore

def build(state, ast, highlight = True):
    state.literals = sorted(state.literals)
    table = list(itertools.product([False, True], repeat=len(state.literals)))
    body, formulas = _build_header(state.literals, ast)
    for values in table:
        binding = dict(zip(state.literals, values))
        body += '\n' + _build_body(binding, formulas, ast, highlight)
    return body

def _build_body(binding, formulas, ast, highlight):
    body = ''
    for key, value in binding.items():
        body += str(int(value)) + ' ' * len(key)
    body += '| '
    offset = len(body)
    body += ' ' * max(formulas.keys())
    main_found = False
    for index, formula in formulas.items():
        if highlight:
            if formula is ast:
                body = body[:offset + index] + Fore.RED + str(int(formula.eval(binding))) + Fore.RESET + body[offset + index + 1:]
                main_found = True
            elif main_found:
                body = body[:offset + index + len(Fore.RED + Fore.RESET)] + str(int(formula.eval(binding))) + body[offset + index + 1 + len(Fore.RED + Fore.RESET):]
            else:
                body = body[:offset + index] + str(int(formula.eval(binding))) + body[offset + index + 1:]
        else:
            body = body[:offset + index] + str(int(formula.eval(binding))) + body[offset + index + 1:]
    return body

def _build_header(literals, ast):
    formulas = {}
    header = ''
    for literal in literals:
        header += literal + ' '
    header += '| ' + ast.to_string(formulas)
    return header, formulas
