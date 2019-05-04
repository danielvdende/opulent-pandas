import pandas as pd
import unittest

from opulent_pandas import (
    InvalidDataError,
    InvalidTypeError,
    MissingColumnError,
    Optional,
    RangeValidator,
    Required,
    Schema,
    TypeValidator,
)


class SchemaTest(unittest.TestCase):

    data = pd.DataFrame({"foo": [1, 2, 3], "bar": [4, 5, 6], "baz": [7, 8, 9]})

    def test_invalid_type_error(self):
        schema = Schema(
            {
                Required("foo"): [TypeValidator(str)],
                Required("bar"): [],
                Required("baz"): [],
            }
        )
        with self.assertRaises(InvalidTypeError) as exc_info:
            schema.validate(self.data)
        self.assertEqual(
            exc_info.exception.msg,
            "Invalid data type found for column: foo. Required type: " "<class 'str'>",
        )

    def test_error_thrown_for_missing_columns(self):
        schema = Schema({Required("foo"): [], Required("bar"): [], Required("qux"): []})
        with self.assertRaises(MissingColumnError) as exc_info:
            schema.validate(self.data)
        self.assertEqual(exc_info.exception.msg, "Columns missing: {'baz'}")

    def test_validation_passes_with_all_columns(self):
        schema = Schema({Required("foo"): [], Required("bar"): [], Optional("baz"): []})
        try:
            schema.validate(self.data)
        except MissingColumnError as e:
            self.fail(f"Validation unexpectedly raised MissingColumnError: {e}")

    def test_validation_exceeds_lower_range(self):
        schema = Schema(
            {
                Required("foo"): [RangeValidator(min=0, max=3)],
                Required("bar"): [RangeValidator(min=4, max=6)],
                Required("baz"): [RangeValidator(min=8, max=9)],
            }
        )
        with self.assertRaises(InvalidDataError) as exc_info:
            schema.validate(self.data)
        self.assertEqual(
            exc_info.exception.msg,
            "Value found smaller than enforced minimum for column: baz. "
            "Required minimum: 8",
        )

    def test_validation_exceeds_upper_range(self):
        schema = Schema(
            {
                Required("foo"): [RangeValidator(min=0, max=3)],
                Optional("bar"): [RangeValidator(min=4, max=6)],
                Optional("baz"): [RangeValidator(min=7, max=8)],
                Optional("qux"): [TypeValidator(str)],
            }
        )
        with self.assertRaises(InvalidDataError) as exc_info:
            schema.validate(self.data)
        self.assertEqual(
            exc_info.exception.msg,
            "Value found larger than enforced maximum for column: baz. "
            "Required maximum: 8",
        )

    def test_get_required_columns(self):
        schema = Schema(
            {
                Required("foo"): [RangeValidator(min=0, max=3)],
                Optional("bar"): [RangeValidator(min=4, max=5)],
            }
        )
        expected_result = {"foo"}
        result = schema.get_column_names(Required)

        self.assertEquals(result, expected_result)
