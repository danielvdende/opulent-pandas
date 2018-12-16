
class Error(Exception):
    """
    Base exception
    """
    def __init__(self, msg):
        self.msg = msg


class MissingColumnError(Error):
    """
    Error indicating one or more columns are missing
    """


class InvalidDataError(Error):
    """
    Error indicating the data is not valid in some way.
    """
