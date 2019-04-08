import pandas as pd

from opulent_pandas.column import ColumnType, Required, Optional
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
        # TODO: need to split out required vs optional
        for col, validators in self.schema.items():
            if isinstance(col, Required) or (
                isinstance(col, Optional) and col.column_name in list(df)
            ):
                for validator in validators:
                    validator.validate(df[col.column_name])

    def check_column_presence(self, df: pd.DataFrame):
        # check if all Required columns are there
        if not set(df).issuperset(self.get_column_names(Required)):
            missing_columns = set(df) - self.get_column_names(Required)
            raise MissingColumnError(f"Columns missing: {missing_columns}")

    def get_column_names(self, column_type: ColumnType) -> set:
        columns = set()
        for key in self.schema:
            if isinstance(key, column_type):
                columns.add(key.column_name)
        return columns
