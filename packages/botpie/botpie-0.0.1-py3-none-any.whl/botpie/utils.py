import sys

from collections import namedtuple

def tonamedtuple(typename, obj):
    """Creates and initializes a new namedtuple using typename and obj
    """

    objtuple = namedtuple(typename, list(obj))
    return objtuple(**obj)

def splitmessage(message):
    """Returns a tuple containing the command and arguments from a message.
    Returns None if there is no firstword found
    """

    assert isinstance(message, str)
    words = message.split()
    if words:
        return (words[0], words[1:])

def asserterror(condition, exception):
    """Behaves like assert but raises the passed in exception rather than
    raising AssertError
    """
    if not condition:
        raise exception

def argvstr(argv=None, shift=0):
    """Takes argv and returns the args as a string.
    """
    argv = argv or sys.argv
    return " ".join(argv[shift+1:])