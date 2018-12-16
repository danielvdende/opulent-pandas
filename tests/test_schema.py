import pandas as pd
import unittest

from opulent_pandas.schema import Schema
from opulent_pandas.error import MissingColumnError


class SchemaTest(unittest.TestCase):

    data = pd.DataFrame({'foo': [1, 2, 3], 'bar': [4, 5, 6], 'baz': [7, 8, 9]})

    def test_error_thrown_for_missing_columns(self):
        schema = Schema({
            'foo': [],
            'bar': []
        })
        with self.assertRaises(MissingColumnError):
            schema.validate(self.data)
