import pandas as pd
import unittest

from opulent_pandas.error import InvalidDataError, InvalidTypeError
from opulent_pandas.validator import SetMemberValidator, TypeValidator, RangeValidator, ValueLengthValidator


class TypeValidatorTest(unittest.TestCase):
    validator = TypeValidator(str)

    def test_valid_data(self):
        data = pd.Series(['hello', 'there'])
        try:
            self.validator.validate(data)
        except InvalidDataError as e:
            self.fail(f"Validation unexpected failed type check: {e}")

    def test_all_invalid_types(self):
        data = pd.Series([1, 2, 3])
        with self.assertRaises(InvalidTypeError):
            self.validator.validate(data)

    def test_some_invalid_types(self):
        data = pd.Series(["hello", "there", 3])
        with self.assertRaises(InvalidTypeError):
            self.validator.validate(data)


class RangeValidatorTest(unittest.TestCase):
    validator = RangeValidator(min=-2, max=2)

    def test_valid_data(self):
        data = pd.Series([-1, 0, 1])
        try:
            self.validator.validate(data)
        except InvalidDataError as e:
            self.fail(f"Validation unexpectedly failed range check: {e}")

    def test_data_exceeds_lower_bound(self):
        data = pd.Series([0, 2, -4])
        with self.assertRaises(InvalidDataError):
            self.validator.validate(data)

    def test_data_exceeds_upper_bound(self):
        data = pd.Series([0, 2, 4])
        with self.assertRaises(InvalidDataError):
            self.validator.validate(data)


class ValueLengthValidatorTest(unittest.TestCase):
    validator = ValueLengthValidator(min_length=0, max_length=2)

    def test_valid_values(self):
        data = pd.Series(['ab', 'cd'])
        try:
            self.validator.validate(data)
        except InvalidDataError as e:
            self.fail(f"Validation unexpected failed value length check: {e}")

    def test_value_too_long(self):
        data = pd.Series(['ab', 'cde'])
        with self.assertRaises(InvalidDataError):
            self.validator.validate(data)


class SetMemberValidatorTest(unittest.TestCase):
    validator = SetMemberValidator(('super', 'awesome', 'values'))

    def test_valid_values(self):
        data = pd.Series(['super', 'values'])
        try:
            self.validator.validate(data)
        except InvalidDataError as e:
            self.fail(f"Validation unexpectedly failed set membership check: {e}")

    def test_unknown_values(self):
        data = pd.Series(['super', 'bad', 'values'])
        with self.assertRaises(InvalidDataError):
            self.validator.validate(data)
