# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""Package that defines a collection of assertions usable in Checkers tests.

Note that this is just provided for convenience; you are welcome to use whatever
assert engine you like to make assertions within tests. For example, PyHamcrest
(https://pypi.python.org/pypi/PyHamcrest) is a popular option.
"""

import contextlib


@contextlib.contextmanager
def expect_exception(exception_type):
  """Asserts that an exception of a given type is actually raised.
  
  This is a context-managed assert, so use within a with statement.
  Example:
    with asserts.expect_exception('ZeroDivisionError'):
      2 / 0

  Args:
    exception_type: (type) The type of the expected exception.

  Raises:
    AssertionError: The expected exception isn't raised.
  """
  message = 'expected exception %s to be raised...it wasn\'t' % exception_type
  try:
    yield
  except exception_type:
    return  # Nothing to do; correct exception was raised.
  except Exception as ex:
    message += '; unexpected exception: <%s>' % ex
  raise AssertionError(message)

def is_true(condition, message=None):
  """Asserts that the given condition is true (or at least truthy)."""
  if not message:
    message = 'expected True (or truthy value); got <%s>' % condition
  if not condition:
    raise AssertionError(message)


def is_false(condition, message=None):
  """Asserts that the given condition is false (or at least falsey)."""
  if not message:
    message = 'expected False (or falsey value); got <%s>' % condition
  if condition:
    raise AssertionError(message)


def are_equal(a, b, message=None):
  """Asserts that the two values are equal to each other (using ==)."""
  if not message:
    message = 'expected equality; <%s> != <%s>' % (a, b)
  if a != b:
    raise AssertionError(message)


def are_not_equal(a, b, message=None):
  """Asserts that the two values are not equal to each other (using ==)."""
  if not message:
    message = 'expected non-equality; <%s> == <%s>' % (a, b)
  if a == b:
    raise AssertionError(message)


def is_in(item, collection, message=None):
  """Asserts that the item is in the given collection (using in keyword)."""
  if not message:
    message = 'expected item to be present; <%s> is not in <%s>' % (
        item, collection)
  if item not in collection:
    raise AssertionError(message)


def is_not_in(item, collection, message=None):
  """Asserts that the item is not in the given collection (using in keyword)."""
  if not message:
    message = 'did not expect item to be present; <%s> is in <%s>' % (
        item, collection)
  if item in collection:
    raise AssertionError(message)


def is_empty(collection, message=None):
  """Asserts that the given collection has 0 items (using len)."""
  if not message:
    message = 'expected empty; size is %d <%s>' % (len(collection), collection)
  if len(collection) != 0:  # pylint: disable=g-explicit-length-test
    raise AssertionError(message)


def is_not_empty(collection, message=None):
  """Asserts that the given collection has more than 0 items (using len)."""
  if not message:
    message = 'expected not empty; size is %d <%s>' % (
        len(collection), collection)
  if not collection:
    raise AssertionError(message)


def is_none(x, message=None):
  """Asserts that the given variable has a None value."""
  if not message:
    message = 'expected None; got %s' % x
  if x is not None:
    raise AssertionError(message)


def is_not_none(x, message=None):
  """Asserts that the given variable does not have a None value."""
  if not message:
    message = 'expected non-None value; got %s' % x
  if x is None:
    raise AssertionError(message)


def are_same(a, b, message=None):
  """Asserts that the two values are the same item (using is keyword)."""
  if not message:
    message = 'expected same object; %s and %s are different' % (a, b)
  if a is not b:
    raise AssertionError(message)


def are_not_same(a, b, message=None):
  """Asserts that the two values are not the same item (using is keyword)."""
  if not message:
    message = 'expected different objects; %s and %s are the same' % (a, b)
  if a is b:
    raise AssertionError(message)


def has_length(collection, expected_length, message=None):
  """Asserts that the collection has the given length."""
  if not message:
    message = 'expected length <%d>; got length <%d> for <%s>' % (
        expected_length, len(collection), collection)
  if len(collection) != expected_length:
    raise AssertionError(message)

