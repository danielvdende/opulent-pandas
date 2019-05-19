import pandas as pd

from opulent_pandas.error import (
    AnyInvalidError,
    Error,
    InvalidTypeError,
    MissingTimezoneError,
    RangeError,
    SetMemberError,
    ValueLengthError,
)
from typing import List


class BaseValidator(object):
    """Base validator object"""


class GroupValidator(BaseValidator):
    """Group validator base object, that can be used to combine multiple validators"""


class Any(GroupValidator):
    def __init__(self, validators: List[BaseValidator]):
        self.validators = validators

    def validate(self, df_column: pd.Series):
        errors = []
        for sub_validator in self.validators:
            try:
                sub_validator.validate(df_column)
                # if no exception comes from this, we've found a passing condition
                print("valid validator found", sub_validator)
                return
            except Error as e:
                # append the error to the list
                errors.append(e)

        if len(errors) != 0:
            # some error happened
            raise AnyInvalidError(errors)


class All(GroupValidator):
    def __init__(self, validators: List[BaseValidator]):
        self.validators = validators

    def validate(self, df_column: pd.Series):
        for sub_validator in self.validators:
            # if any validator fails, an error will be raised and thrown.
            sub_validator.validate(df_column)


class TypeValidator(BaseValidator):
    """
    Checks that the dataframe column is of a certain type
    """

    def __init__(self, valid_type: type):
        self.valid_type = valid_type

    def validate(self, df_column: pd.Series):
        if not (df_column.apply(type) == self.valid_type).all():
            raise InvalidTypeError(
                f"Invalid data type found for column: {df_column.name}. "
                f"Required type: {self.valid_type}"
            )


class RangeValidator(BaseValidator):
    """
    Checks that the dataframe column values are between min and max values
    """

    def __init__(self, min: int = None, max: int = None):
        self.min = min
        self.max = max

    def validate(self, df_column: pd.Series):
        if self.min:
            if not (df_column >= self.min).all():
                raise RangeError(
                    f"Value found smaller than enforced minimum for column: {df_column.name}. "
                    f"Required minimum: {self.min}"
                )
        if self.max:
            if not (df_column <= self.max).all():
                raise RangeError(
                    f"Value found larger than enforced maximum for column: {df_column.name}. "
                    f"Required maximum: {self.max}"
                )


class ValueLengthValidator(BaseValidator):
    """
    Checks that all values in the dataframe column are between min and max length values
    This validator will only work if the column value allows for the 'len' function to be applied
    """

    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, df_column: pd.Series):
        if self.min_length:
            if not (df_column.apply(len) >= self.min_length).all():
                raise ValueLengthError(
                    f"Value found with length smaller than enforced minimum length for "
                    f"column: {df_column.name}. Minimum Length: {self.min_length}"
                )
        if self.max_length:
            if not (df_column.apply(len) <= self.max_length).all():
                raise ValueLengthError(
                    f"Value found with length larger than enforced maximum length for "
                    f"column: {df_column.name}. Maximum Length: {self.max_length}"
                )


class SetMemberValidator(BaseValidator):
    """
    Checks that all values in the dataframe column are members of a provided set of valid values
    """

    def __init__(self, values: set):
        self.values = values

    def validate(self, df_column: pd.Series):
        if not df_column.isin(self.values).all():
            raise SetMemberError(
                f"Value found outside of defined set for column: {df_column.name}. "
                f"Allowed: {self.values}"
            )


class TimezoneValidator(BaseValidator):
    """
    Checks that all values in the dataframe column have timezone information
    TODO: extend to allow required timezone as a parameter, e.g. check that the timezone is correct
    """

    def validate(self, df_column: pd.Series):
        if not df_column.dt.tz:
            raise MissingTimezoneError(
                f"Non-timezone-aware dates found for column: {df_column.name}."
            )
