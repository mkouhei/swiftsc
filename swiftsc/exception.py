# -*- coding: utf-8 -*-
"""swiftsc exception module."""


class Error(Exception):
    """Base error class.

    Child classes should define an status code, title, and message_format.
    """

    def __init__(self, message=None):
        """constructor of Error."""
        super(Error, self).__init__(message)


class ValidationError(Error):
    """Not found key."""

    pass


class AuthenticationError(Error):
    """Authentication failed."""

    pass
