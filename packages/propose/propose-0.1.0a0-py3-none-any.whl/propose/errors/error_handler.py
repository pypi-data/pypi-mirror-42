import sys
import traceback

from colorama import Fore, Style

class ErrorHandler:
    def __init__(self, e: Exception, exit: bool = True):
        self.e = e
        self.exit = exit

    def call(self):
        print(self)
        if self.exit:
            sys.exit()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""
{len(self._e_type()) * '-'}
{Fore.RED + self._e_type() + Fore.RESET}
{len(self._e_type()) * '-'}

Propose has catched an error. Here is some additional information:
{Style.BRIGHT + str(self.e) + Style.RESET_ALL}

Output the stacktrace by setting the -t flag."""

    def _e_type(self):
        return type(self.e).__name__
