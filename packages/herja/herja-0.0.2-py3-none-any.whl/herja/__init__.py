"""A module of common python code for heroes."""


import logging
import os
import subprocess

from .assertions import assert_type
from .conversions import to_bytes, to_str


__all__ = [
    'decorators',
    'execute',
    'os',
    'quotify'
]


def execute(args, blocking=True, cwd=None):
    """
    Execute a command as if it were being interpreted by a command line.

    :return: (stdout, stderr, returncode) if blocking else None
    """
    if cwd is None:
        cwd = os.getcwd()

    assert_type(args, list)

    # force everything into byte strings
    args = [to_bytes(arg) for arg in args]

    # log the execution information
    logging.info('[%s]$ %s', os.path.basename(cwd), ' '.join(quotify(to_str(a)) for a in args))

    if not blocking:
        return subprocess.Popen(args, cwd=cwd)

    # create the subprocess
    p = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd
    )

    # obtain the stdout and stderr bytes objects with communicate()
    stdout, stderr = p.communicate()

    # return two bytes objects and an integer
    return stdout, stderr, p.returncode


def quotify(data):
    """Wrap a string or bytes in quotes, if a space is inside."""
    assert_type(data, bytes, str)

    if isinstance(data, bytes):
        quote, space = b'"', b' '
    elif isinstance(data, str):
        quote, space = '"', ' '

    if space in data:
        return quote + data + quote
    return data
