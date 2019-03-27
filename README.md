[![Build Status](https://travis-ci.com/danielvdende/opulent-pandas.svg?token=km81qsbsLrgZWGfcfi7a&branch=master)](https://travis-ci.com/danielvdende/opulent-pandas)
[![PyPI version](https://badge.fury.io/py/opulent-pandas.svg)](https://badge.fury.io/py/opulent-pandas)
# Opulent-Pandas
Opulent-Pandas is a schema validation packages aimed specifically at validating the schema of pandas dataframes. 
It takes heavy inspiration from [voluptuous](), and tries to stay as close as possible to the API defined in this package. Opulent-Pandas
is different from voluptuous in that it heavily relies on [Pandas]() to perform the validation. This makes Opulent-Pandas considerably faster
than voluptuous on larger datasets. It does, however, mean that the input format is also a Pandas DataFrame, rather than a dict (as is the case for voluptuous)
A performance comparison of voluptuous and Opulent-Pandas can be found [here]()

## Example
Defining a schema in Opulent-Pandas is very similar to how you would in [voluptuous](). To make the similarities and differences clear, let's walk through the same example as is done in the voluptuous readme.
 
Twitter's [user search API](https://dev.twitter.com/rest/reference/get/users/search) accepts
query URLs like:

```
$ curl 'https://api.twitter.com/1.1/users/search.json?q=python&per_page=20&page=1'
```

To validate this we might use a schema like:

```pycon
>>> from opulent_pandas import Schema, TypeValidator, Required
>>> schema = Schema({
...   Required('q'): [TypeValidator(str)],
...   Required('per_page'): [TypeValidator(int)],
...   Required('page'): [TypeValidator(int)],
... })

```
Comparing with voluptuous, you'll notice a few things:
1. The validators per field are always specified as a list.

If we look at the more complex schema, as defined in the readme of voluptuous, we see very similar schemas:

```pycon
>>> from opulent_pandas.validator import Required, RangeValidator, TypeValidator, ValueLengthValidator 
>>> schema = Schema({
...   Required('q'): [TypeValidator(str), ValueLengthValidator(min_length=1)),
...   Required('per_page'): [TypeValidator(int), RangeValidator(min=1, max=20)),
...   Required('page'): [TypeValidator(int), RangeValidator(min=0)),
... })

```

If you pass data in that does not satisfy the requirements specified in your Opulent-Pandas schema, you'll get a corresponding error message:

There are 3 required fields:

```pycon
>>> from opulent_pandas import MissingColumnError
>>> try:
...   schema.validate({})
...   raise AssertionError('MissingColumnError not raised')
... except MissingColumnError as e:
...   exc = e
>>> str(exc) == "Columns missing"
True

```

`q` must be a string:

```pycon
>>> try:
...   schema.validate(pd.DataFrame({'q': [123], 'per_page':[10], 'page': [1]})
...   raise AssertionError('InvalidTypeError not raised')
... except InvalidTypeError as e:
...   exc = e
>>> str(exc) == "Invalid data type found. Required: <class 'str'>"
True

```

...and must be at least one character in length:

```pycon
>>> try:
...   schema({'q': ''})
...   raise AssertionError('MultipleInvalid not raised')
... except MultipleInvalid as e:
...   exc = e
>>> str(exc) == "length of value must be at least 1 for dictionary value @ data['q']"
True
>>> schema({'q': '#topic'}) == {'q': '#topic', 'per_page': 5}
True

```

"per\_page" is a positive integer no greater than 20:

```pycon
>>> try:
...   schema({'q': '#topic', 'per_page': 900})
...   raise AssertionError('MultipleInvalid not raised')
... except MultipleInvalid as e:
...   exc = e
>>> str(exc) == "value must be at most 20 for dictionary value @ data['per_page']"
True
>>> try:
...   schema({'q': '#topic', 'per_page': -10})
...   raise AssertionError('MultipleInvalid not raised')
... except MultipleInvalid as e:
...   exc = e
>>> str(exc) == "value must be at least 1 for dictionary value @ data['per_page']"
True

```

"page" is an integer \>= 0:

```pycon
>>> try:
...   schema({'q': '#topic', 'per_page': 'one'})
...   raise AssertionError('MultipleInvalid not raised')
... except MultipleInvalid as e:
...   exc = e
>>> str(exc)
"expected int for dictionary value @ data['per_page']"
>>> schema({'q': '#topic', 'page': 1}) == {'q': '#topic', 'page': 1, 'per_page': 5}
True

```