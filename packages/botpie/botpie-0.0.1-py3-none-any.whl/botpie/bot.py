import json

from .cmd import Command, CommandParser, Response
from .utils import splitmessage, asserterror
from .exception import InvalidCommandError, DuplicateCommandError, \
    CommandNotFoundError

class Bot:
    """The public interface for performing all bot operations

    Parameters:
        nickname (str):
            A nickname for the bot. Default: 'Bot'
        description (str):
            Brief description for the bot. Default: None
        commands (list):
            Commands for the bot to listen for and execute. Default: []
        command_pattern (str):
            Regex pattern used for validating a command name. Default will
            match any non-whitespace word.
        command_prefix (str):
            Special characters to prepend to the command. If a value is
            provided, it will be stripped from the command name and
            re-prepended. Default: None
        add_help (boolean):
            If True, automatically adds a helper argument (-h/--help) to all
            commands. Default: False
        quiet (boolean):
            If True, Bot will not add errors to the message string.
            Default: True
    """

    def __init__(self,
        nickname="Bot",
        description=None,
        command_pattern="^\S+$",
        command_prefix=None,
        add_help=False,
        quiet=True):

        self.nickname = nickname
        self.description = description
        self.command_pattern = command_pattern
        self.command_prefix = command_prefix
        self.add_help = add_help
        self.quiet = quiet

        # Maps the command name keys to their Command instances
        self._registered_commands = {}

        #: Maps the handler name keys to their functions
        self._registered_handlers = {}

        # Temporary storage for decorator arguments
        self._decargs = {}

    @property
    def commands(self):
        return sorted(list(self._registered_commands.values()))

    def getcommand(self, name, default=None):
        return self._registered_commands.get(name, default)

    def gethandler(self, commandname, default=None):
        return self._registered_handlers.get(commandname, default)

    def addcommand(self, commandname, args=None, handler=None,
        add_help=False):
        """Takes a command, parses it, and adds it to the listen list
        """

        add_help = add_help or self.add_help

        args = args or []
        # Name validation can happen here eventually, but for now this
        # just checks for an empty string
        asserterror(commandname, InvalidCommandError)

        command = Command(commandname, args=args, add_help=add_help)

        if commandname in self._registered_commands:
            msg = "command '{}' already exists"
            raise DuplicateCommandError(msg.format(command))

        if callable(handler):
            self._registered_handlers.setdefault(command.name, handler)
        elif handler != None:
            raise TypeError("response must be callable")

        self._registered_commands.setdefault(command.name, command)

        return command

    def delcommand(self, commandname):
        try:
            self._registered_commands.pop(commandname)
        except KeyError as ke:
            raise CommandNotFoundError(commandname)

    def runcommand(self, commandname, args=None):
        """If the command is registered, then it is executed here.
        """

        command = self.getcommand(commandname)
        asserterror(command, CommandNotFoundError(command))

        args = args or []
        parsed = command.parse_args(args)

        if parsed.error:
            if self.quiet:
                return Response(error=parsed.error)
            return Response(str(parsed.error), error=parsed.error)

        if getattr(parsed.args, "help", False):
            return Response(command.format_help())

        handler = self.gethandler(command.name)

        # Bot will do nothing if no handler is registered. This may be
        # changed to require a handler to be registed if a command already
        # is
        if handler:
            argsdict = parsed.args._asdict()

            if command.add_help:
                _pop = argsdict.pop("help", None)

            return Response(str(handler(**argsdict)))

    def isregistered(self, command):
        """Checks if the command is already registed.
        Returns True if the command is found
        """

        if command and command in self._registered_commands:
            return True
        return False

    def inspect(self, message):
        """Reads *message* for a command, executes the command if one is
        found, and returns a Result instance. Returns None if the bot has
        nothing to do. For applications which only need the string message
        as a result, using the *inspectstr* is recommended.
        """
        splitmsg = splitmessage(message)

        if splitmsg:
            (commandname, args) = splitmsg

            if self.isregistered(commandname):
                return self.runcommand(commandname, args=args)

    def inspectstr(self, message):
        """Performs the same function as *inspect* and returns just the
        message portion as an str. If no result is found, the string will
        be empty.
        """
        return getattr(self.inspect(message), "message", "")

    def command(self, commandname, *args, **kwargs):
        def decorator(func):
            cmd = self.addcommand(commandname, *args, handler=func, **kwargs)
            argslist = self._decargs.get(func.__name__, [])
            for arg in reversed(argslist):
                cmd.addargument(*arg[0], **arg[1])
            _pop = self._decargs.pop(func.__name__, None)
            return func
        return decorator

    def argument(self, *args, **kwargs):
        def decorator(func):
            self._decargs.setdefault(func.__name__, [])
            self._decargs[func.__name__].append((args, kwargs))
            return func
        return decorator


# Placeholders for now
class DiscordBot(Bot):
    pass


class IRCBot(Bot):
    pass


class TwitchBot(Bot):
    pass