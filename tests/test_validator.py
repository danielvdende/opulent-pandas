import pandas as pd
import unittest

from opulent_pandas.error import InvalidDataError, InvalidTypeError, AnyInvalidError, MissingTimezoneError
from opulent_pandas.validator import (All, Any, SetMemberValidator, TimezoneValidator, TypeValidator,
                                      RangeValidator, ValueLengthValidator)


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


class AllValidatorTest(unittest.TestCase):
    single_group_validator = All([SetMemberValidator(('foo', 'bar')), ValueLengthValidator(min_length=3)])
    nested_group_validator = All([RangeValidator(min=0), All([TypeValidator(valid_type=int),
                                                              RangeValidator(max=3)])])

    def test_all_valid_single_group(self):
        data = pd.Series(['foo', 'foo', 'bar'])
        try:
            self.single_group_validator.validate(data)
        except InvalidDataError as e:
            self.fail(f'Validation unexpectedly failed: {e}')

    def test_some_invalid_single_group(self):
        data = pd.Series(['foo', 'bar', 'baz'])
        with self.assertRaises(InvalidDataError):
            self.single_group_validator.validate(data)

    def test_all_valid_nested_group(self):
        data = pd.Series([1, 2, 1, 3])
        try:
            self.nested_group_validator.validate(data)
        except InvalidDataError as e:
            self.fail(f'Validation unexpectedly failed: {e}')

    def test_some_invalid_nested_group(self):
        data = pd.Series([1, 2, 1, 4])
        with self.assertRaises(InvalidDataError):
            self.nested_group_validator.validate(data)


class AnyValidatorTest(unittest.TestCase):
    single_group_validator = Any([SetMemberValidator(('foo', 'bar')), ValueLengthValidator(min_length=2)])
    nested_group_validator = Any([TypeValidator(str), All([TypeValidator(valid_type=int),
                                                           RangeValidator(min=0)])])

    def test_all_valid_single_group(self):
        data = pd.Series(['foo', 'foo', 'bar', 'fa'])
        try:
            self.single_group_validator.validate(data)
        except AnyInvalidError as e:
            self.fail(f'Validation unexpectedly failed: {e}')

    def test_some_invalid_single_group(self):
        data = pd.Series(['foo', 'bar', 'baz', 'f'])
        with self.assertRaises(AnyInvalidError):
            self.single_group_validator.validate(data)

    def test_all_valid_nested_group(self):
        data = pd.Series([1, 2, 1, 3])
        try:
            self.nested_group_validator.validate(data)
        except AnyInvalidError as e:
            self.fail(f'Validation unexpectedly failed: {e}')

    def test_some_invalid_nested_group(self):
        data = pd.Series([1, 2, 1, 4, 'foobar'])
        with self.assertRaises(AnyInvalidError):
            self.nested_group_validator.validate(data)


class TimezoneValidatorTest(unittest.TestCase):
    validator = TimezoneValidator()

    def test_timezone_aware_date(self):
        date_field = pd.to_datetime("28-08-1990 12:22", format="%d-%m-%Y %H:%M")\
            .tz_localize("Europe/Amsterdam")
        valid_data = pd.Series([date_field])

        try:
            self.validator.validate(valid_data)
        except InvalidDataError as e:
            self.fail(f'Validation unexpectedly failed: {e}')

    def test_timezone_unaware_date(self):
        date_field = pd.to_datetime("28-08-1990 12:22", format="%d-%m-%Y %H:%M")
        invalid_data = pd.Series([date_field])

        with self.assertRaises(MissingTimezoneError):
            self.validator.validate(invalid_data)
