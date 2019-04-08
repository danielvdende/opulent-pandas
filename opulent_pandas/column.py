class ColumnType(object):
    def __init__(self, column_name, description=""):
        self.column_name = column_name
        self.description = description


class Required(ColumnType):
    """

    """


class Optional(ColumnType):
    """

    """
