import pandas as pd
import unittest

from opulent_pandas.schema import Schema
from opulent_pandas.error import InvalidDataError, MissingColumnError
from opulent_pandas.validator import RangeValidator


class SchemaTest(unittest.TestCase):

    data = pd.DataFrame({'foo': [1, 2, 3], 'bar': [4, 5, 6], 'baz': [7, 8, 9]})

    def test_error_thrown_for_missing_columns(self):
        schema = Schema({
            'foo': [],
            'bar': []
        })
        with self.assertRaises(MissingColumnError):
            schema.validate(self.data)

    def test_validation_passes_with_all_columns(self):
        schema = Schema({
            'foo': [],
            'bar': [],
            'baz': []
        })
        try:
            schema.validate(self.data)
        except MissingColumnError as e:
            self.fail(f'Validation unexpectedly raised MissingColumnError: {e}')

    def test_validation_exceeds_lower_range(self):
        schema = Schema({
            'foo': [RangeValidator(min=0, max=3)],
            'bar': [RangeValidator(min=4, max=6)],
            'baz': [RangeValidator(min=8, max=9)]
        })
        with self.assertRaises(InvalidDataError):
            schema.validate(self.data)

    def test_validation_exceeds_upper_range(self):
        schema = Schema({
            'foo': [RangeValidator(min=0, max=3)],
            'bar': [RangeValidator(min=4, max=6)],
            'baz': [RangeValidator(min=7, max=8)]
        })
        with self.assertRaises(InvalidDataError):
            schema.validate(self.data)
