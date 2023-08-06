from .parser import Parser
from .state import State

parser = Parser().get_parser()

def parse(input, tokens, state = State()):
    return parser.parse(tokens, state)
