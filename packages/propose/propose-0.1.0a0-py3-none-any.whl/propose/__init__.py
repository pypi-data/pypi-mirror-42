"""Propose

Usage:
  propose <formula> [-f]

Options:
  -h --help     Show this.
  --version     Show version.
  -f --file     Pass a file instead of an inline formula.

"""

name = 'propose'

import pathlib
import warnings
warnings.filterwarnings('ignore')

from docopt import docopt
from colorama import init
init()

from propose.builder import build
from propose.lexer import lex
from propose.parser import parse, State

def _version():
    return 'Propose ' + _read_file(pathlib.Path(__file__).parent / 'VERSION').replace('\n', '')

def _read_file(filename):
    try:
        with open(filename) as file:
            return file.read()
    except Exception as e:
        ErrorHandler(e).call()

def main():
    args = docopt(__doc__, version=_version())

    if args['--file']:
        input = _read_file(args['<formula>'])
    else:
        input = args['<formula>']
    tokens = lex(input)
    state = State()
    ast = parse(input, tokens, state)

    print(build(state, ast))
