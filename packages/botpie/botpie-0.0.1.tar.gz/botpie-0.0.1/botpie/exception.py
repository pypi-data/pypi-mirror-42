class ParserExitError(Exception):
    pass

class ParserUnknownError(Exception):
    pass

class CommandError(Exception):
    pass

class CommandNotFoundError(Exception):
    pass

class DuplicateCommandError(Exception):
    pass

class InvalidCommandError(Exception):
    pass