import argparse as _argparse
import re as _re

from .exception import ParserExitError
from .utils import tonamedtuple

class ParsedResult(_argparse._AttributeHolder):
    """The result returned from executing a registered command.

    Attributes:
    *   args:            An Args instance including the parsed arguments from
                         CommandParser
    *   unknowns (list): This will contain any invalid arguments found
    *   error:           If the parser had any problems, this value will be
                         the Exception found
    """

    def __init__(self, args=None, unknowns=None, error=None):
        self.args = args
        if args:
            self.args = tonamedtuple('Args', args.__dict__)
        self.unknowns = unknowns or []
        self.error = error


class CommandParser(_argparse.ArgumentParser):
    """A wrapper for argparse.ArgumentParser which prevents the parser from
    exiting when an exception is raised. This constructor takes the same
    arguments as ArgumentParser

    Ref: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """

    def __init__(self, *args, **kwargs):
        # Store add_help param and set the param to False to prevent
        # ArgumentParser from adding the help argument in on init
        add_help = kwargs.get("add_help", False) # Locking as False for now
        kwargs["add_help"] = False

        super().__init__(*args, **kwargs)

    def parse_args(self, args):
        try:
            (matches, unknowns) = self.parse_known_args(args)
            err = ""
            if unknowns:
                fmt = _argparse._("unrecognized arguments: {}")
                err = fmt.format(" ".join(unknowns))
            return ParsedResult(matches, unknowns, err)
        except ParserExitError as perr:
            return ParsedResult(error=perr)

    def _print_message(self, *args, **kwargs):
        pass

    def _get_dest(self, *args, **kwargs):
        return self._get_optional_kwargs(*args, **kwargs)["dest"]

    def exit(self, status=0, message=None):
        raise ParserExitError(status, message)


class Response:

    def __init__(self, message="", error=None):
        self.message = message
        self.error = error

    def __repr__(self):
        return "Response('{}')".format(self.message)

    def __str__(self):
        return str(self.message)

    def update(self, message):
        self.message = message


class Command(object):
    """A Command to be registered by Bot.

    Parameters:
        name (str):
            The name of the command. Treated as a unique id
        args (list):
            An instance of Args with any arguments if given
        add_help (boolean):
            If True, automatically adds a helper argument (-h/--help) to
            the command. Default: False
    """

    def __init__(self, name, args=None, add_help=False):
        self.error = None
        self._name = str(name)
        self._rargs = args or []
        self._parser = CommandParser(name)

        self.add_help = add_help

        if add_help:
            self.addhelp()

    def __repr__(self):
        fmt = "Command('{}', args={})"
        return fmt.format(self.name, self.args)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._rargs

    def addargument(self, *args, **kwargs):
        self._rargs.append(args)
        self._parser.add_argument(*args, **kwargs)
        return self

    def addhelp(self):
        self.addargument("-h", "--help",
            action="store_true",
            help="show this help message")

    def format_help(self):
        return str(self._parser.format_help())

    def parse_args(self, args):
        return self._parser.parse_args(args)