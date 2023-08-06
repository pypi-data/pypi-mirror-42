def render_tokens(tokens):
    result = ''

    for token in tokens:
        result += str(token) + ': ' + str(token.source_pos) + '\n'

    return result
