# -*- coding: utf-8 -*-
"""
pdnsapi_lib.exception
~~~~~~~~~~~~~~~~~~~~~
"""


class Error(Exception):
    """Base error class.

    Child classes should define an status code, title, and message_format.
    """

    def __init__(self, message=None):
        super(Error, self).__init__(message)


class ValidationError(Error):
    """Not found key """
    pass
