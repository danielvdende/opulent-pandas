[![Build Status](https://travis-ci.com/danielvdende/opulent-pandas.svg?token=km81qsbsLrgZWGfcfi7a&branch=master)](https://travis-ci.com/danielvdende/opulent-pandas)
[![PyPI version](https://badge.fury.io/py/opulent-pandas.svg)](https://badge.fury.io/py/opulent-pandas)
# Opulent-Pandas
Opulent-Pandas is a schema validation packages aimed specifically at validating the schema of pandas dataframes. 
It takes heavy inspiration from [voluptuous](https://github.com/alecthomas/voluptuous), and tries to stay as close as possible to the API defined in this package. Opulent-Pandas
is different from voluptuous in that it heavily relies on [Pandas](https://pandas.pydata.org/) to perform the validation. This makes Opulent-Pandas considerably faster
than voluptuous on larger datasets. It does, however, mean that the input format is also a Pandas DataFrame, rather than a dict (as is the case for voluptuous)
A performance comparison of voluptuous and Opulent-Pandas will be added to this readme soon!

## Example
Defining a schema in Opulent-Pandas is very similar to how you would in voluptuous. To make the similarities and differences clear, let's walk through the same example as is done in the voluptuous readme.
 
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
Comparing with voluptuous, you'll notice that the validators per field are always specified as a list. Other than that,
it's very similar to how you would define the schema with voluptuous

If we look at the more complex schema, as defined in the readme of voluptuous, we see very similar schemas:

```pycon
>>> from opulent_pandas.validator import Required, RangeValidator, TypeValidator, ValueLengthValidator 
>>> schema = Schema({
...   Required('q'): [TypeValidator(str), ValueLengthValidator(min_length=1)],
...   Required('per_page'): [TypeValidator(int), RangeValidator(min=1, max=20)],
...   Required('page'): [TypeValidator(int), RangeValidator(min=0)],
... })

```

One difference between Opulent-Pandas and voluptuous is that Opulent-Pandas has a `validate` function that can be used
to validate a given data structure rather tha voluptuous' approach of passing the data directly to your schema as a parameter. 

If you pass data in that does not satisfy the requirements specified in your Opulent-Pandas schema, you'll get a corresponding error message. Walking
through the examples provided in the voluptuous readme:

There are 3 required fields:
TODO: this example should also tell you which columns are missing. Seems to be a bug.
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
>>> from opulent_pandas import InvalidTypeError
>>> try:
...   schema.validate(pd.DataFrame({'q': [123], 'per_page':[10], 'page': [1]})
...   raise AssertionError('InvalidTypeError not raised')
... except InvalidTypeError as e:
...   exc = e
>>> str(exc) == "Invalid data type found for column: q. Required: <class 'str'>"
True

```

...and must be at least one character in length:

```pycon
>>> from opulent_pandas import ValueLengthError
>>> try:
...   schema.validate(pd.DataFrame({'q': [''], 'per_page': 5, 'page': 12}))
...   raise AssertionError('ValueLengthError not raised')
... except ValueLengthError as e:
...   exc = e
>>> str(exc) == "Value found with length smaller than enforced minimum length for column: q. Minimum Length: 1"
True

```

"per\_page" is a positive integer no greater than 20:

```pycon
>>> from opulent_pandas import RangeError
>>> try:
...    schema.validate(pd.DataFrame({'q': ['#topic'], 'per_page': [900], 'page': [12]}))
...    raise AssertionError('RangeError not raised')
... except RangeError as e:
...    exc = e
>>> str(exc) == "Value found larger than enforced maximum for column: per_page. Required maximum: 20"
True

>>> try:
...    schema.validate(pd.DataFrame({'q': ['#topic'], 'per_page': [-10], 'page': [12]}))
...    raise AssertionError('RangeError not raised')
... except RangeError as e:
...    exc = e
>>> str(exc) == "Value found larger than enforced minimum for column: per_page. Required minimum: 1"
True

```

"page" is an integer \>= 0:

```pycon
>>> try:
...   schema.validate(pd.DataFrame({'q': ['#topic'], 'per_page': ['one']})
...   raise AssertionError('InvalidTypeError not raised')
... except InvalidTypeError as e:
...   exc = e
>>> str(exc) == "Invalid data type found for column: page. Required type: <class 'int'>"
True

```