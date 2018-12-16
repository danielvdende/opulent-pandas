import pandas as pd
from opulent_pandas.error import MissingColumnError


class Schema(object):
    """
    Main class to hold the defined schema
    """

    def __init__(self, schema: dict):
        self.schema = schema

    def validate(self, df: pd.DataFrame):
        # first check if all columns are there
        if not set(self.schema.keys()) == set(list(df)):
            # TODO: better error message here
            raise MissingColumnError("Columns missing")

        # now check any other restrictions on those columns
        for col, validators in self.schema.items():
            for validator in validators:
                validator.validate(df[col])
