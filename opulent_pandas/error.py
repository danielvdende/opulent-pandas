from typing import List


class Error(Exception):
    """
    Base exception
    """

    def __init__(self, msg):
        self.msg = msg


class GroupError(Error):
    """
    Base exception class for group errors
    """

    def __init__(self, errors: List[Error]):
        self.errors = errors


class MissingColumnError(Error):
    """
    Error indicating one or more columns are missing
    """


class InvalidDataError(Error):
    """
    Error indicating the data is not valid in some way.
    """

    def __init__(self, msg):
        Error.__init__(self, msg)


class InvalidTypeError(InvalidDataError):
    """"""


class RangeError(InvalidDataError):
    """"""


class ValueLengthError(InvalidDataError):
    """"""


class SetMemberError(InvalidDataError):
    """"""


class AnyInvalidError(GroupError):
    """"""


class MissingTimezoneError(InvalidDataError):
    """"""
