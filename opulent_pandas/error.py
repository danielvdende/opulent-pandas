
class Error(Exception):
    "Base exception"


class MissingColumnError(Error):
    def __init__(self, msg):
        self.msg = msg
