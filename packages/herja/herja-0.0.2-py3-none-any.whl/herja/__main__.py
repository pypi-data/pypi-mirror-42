from . import execute
from .decorators import MainCommands


@MainCommands()
def main(args):
    """Handle arguments given to this module."""
    execute(['ls', '..'])
    execute(['ls', '../haha *.txt'])
    return 0
