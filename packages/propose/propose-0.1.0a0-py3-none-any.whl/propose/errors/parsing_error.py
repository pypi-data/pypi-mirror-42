from colorama import Style

class ParsingError:
    def __init__(self, e, input):
        self.e = e
        self.input = input

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self._get_sourcepos() is None:
            return 'OH NO! Propose was unable to parse this :/' + Style.RESET_ALL + '\n\nPlease report to https://github.com/jonhue/propose/issues' + '\n\n'
        else:
            return 'Unable to parse "' + self.input[self._get_sourcepos().idx] + '" at position ' + self._pos_str() + '\n\n' + Style.RESET_ALL

    def _get_sourcepos(self):
        return self.e.getsourcepos()

    def _pos_str(self):
        sourcepos = self._get_sourcepos()
        return str(sourcepos.lineno) + ':' + str(sourcepos.colno)
