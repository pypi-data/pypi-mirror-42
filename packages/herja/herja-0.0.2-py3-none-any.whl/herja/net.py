"""A collection of utilities for performing network requests/connections."""


import logging

from requests import Session as RequestsSession

from .constants import HEADER_DEFAULTS


class Session(RequestsSession):

    def __init__(self, header_tuples=None):
        """Initialize a special requests session with the default headers."""
        super(Session, self).__init__()

        for key, value in HEADER_DEFAULTS if header_tuples is None else header_tuples:
            self.headers[key] = value
            logging.debug('Set Header "%s" to "%s"', key, value)
