import pandas as pd

from opulent_pandas.column import ColumnType, Required
from opulent_pandas.error import MissingColumnError


class Schema(object):
    """
    Main class to hold the defined schema
    """

    def __init__(self, schema: dict):
        self.schema = schema

    def validate(self, df: pd.DataFrame):
        # first check if all columns are there
        self.check_column_presence(df)

        # now check any other restrictions on those columns
        for col, validators in self.schema.items():
            for validator in validators:
                validator.validate(df[col.column_name])

    def check_column_presence(self, df: pd.DataFrame):
        # check if all Required columns are there
        if not set(df).issuperset(self.get_column_names(Required)):
            raise MissingColumnError("Columns missing")

    def get_column_names(self, column_type: ColumnType) -> set:
        columns = set()
        for key in self.schema:
            if isinstance(key, column_type):
                columns.add(key.column_name)
        return columns
