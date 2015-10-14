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

"""Tests for checkers.asserts."""

import checkers
from checkers import asserts
from checkers.runners import pyunit

TRUTHY_VALUES = {
    'bool': {'value': True},
    'int': {'value': 2},
    'string': {'value': 'hello'},
    'list': {'value': [0]},
    'dict': {'value': {'': ''}},
}

FALSEY_VALUES = {
    'bool': {'value': False},
    'int': {'value': 0},
    'string': {'value': ''},
    'list': {'value': []},
    'dict': {'value': {}},
}

EQUAL_VALUES = {
    'int': {'x': 0, 'y': 0},
    'list': {'x': [1, 2, 4, 8], 'y': [1, 2, 4, 8]},
}

UNEQUAL_VALUES = {
    'int': {'x': 0, 'y': 1},
    'list': {'x': [0, 2, 4, 8], 'y': [1, 2, 4, 8]},
}

CONTAINS_VALUES = {
    'string': {'item': 'e', 'collection': 'hello'},
    'list': {'item': 2, 'collection': [0, 2, 4, 8]},
    'dict': {'item': 'foo', 'collection': {'foo': True, 'bar': False}}
}

MISSING_VALUES = {
    'string': {'item': 'w', 'collection': 'hello'},
    'list': {'item': 1, 'collection': [0, 2, 4, 8]},
    'dict': {'item': 'baz', 'collection': {'foo': True, 'bar': False}}
}

DIFFERENT_INSTANCE_VALUES = {
    'list': {'x': [0, 2, 4, 8], 'y': [0, 2, 4, 8]},
}

EMPTY_VALUES = {
    'empty_list': {'length': 0, 'collection': []},
    'empty_string': {'length': 0, 'collection': ''},
    'empty_dict': {'length': 0, 'collection': {}}
}

NONEMPTY_VALUES = {
    'nonempty_list': {'length': 2, 'collection': [0, 1]},
    'nonempty_string': {'length': 12, 'collection': 'hello, world'},
}


@checkers.parameterize(TRUTHY_VALUES)
@checkers.test
def test_is_true_ok(value):
  asserts.is_true(value)


@checkers.parameterize(FALSEY_VALUES)
@checkers.test
def test_is_true_fail(value):
  with asserts.expect_exception(AssertionError):
    asserts.is_true(value)


@checkers.parameterize(FALSEY_VALUES)
@checkers.test
def test_is_false_ok(value):
  asserts.is_false(value)


@checkers.parameterize(TRUTHY_VALUES)
@checkers.test
def test_is_false_fail(value):
  with asserts.expect_exception(AssertionError):
    asserts.is_false(value)


@checkers.parameterize(EQUAL_VALUES)
@checkers.test
def test_assert_equal_ok(x, y):
  asserts.are_equal(x, y)


@checkers.parameterize(UNEQUAL_VALUES)
@checkers.test
def test_assert_equal_bad(x, y):
  with asserts.expect_exception(AssertionError):
    asserts.are_equal(x, y)


@checkers.parameterize(UNEQUAL_VALUES)
@checkers.test
def test_assert_not_equal_ok(x, y):
  asserts.are_not_equal(x, y)


@checkers.parameterize(EQUAL_VALUES)
@checkers.test
def test_assert_not_equal_bad(x, y):
  with asserts.expect_exception(AssertionError):
    asserts.are_not_equal(x, y)


@checkers.parameterize(CONTAINS_VALUES)
@checkers.test
def test_assert_in_ok(item, collection):
  asserts.is_in(item, collection)


@checkers.parameterize(MISSING_VALUES)
@checkers.test
def test_assert_in_bad(item, collection):
  with asserts.expect_exception(AssertionError):
    asserts.is_in(item, collection)


@checkers.parameterize(MISSING_VALUES)
@checkers.test
def test_assert_not_in_ok(item, collection):
  asserts.is_not_in(item, collection)


@checkers.parameterize(CONTAINS_VALUES)
@checkers.test
def test_assert_not_in_bad(item, collection):
  with asserts.expect_exception(AssertionError):
    asserts.is_not_in(item, collection)


@checkers.parameterize(EMPTY_VALUES)
@checkers.test
def test_assert_empty_ok(collection):
  asserts.is_empty(collection)


@checkers.parameterize(NONEMPTY_VALUES)
@checkers.test
def test_assert_empty_bad(collection):
  with asserts.expect_exception(AssertionError):
    asserts.is_empty(collection)


@checkers.parameterize(NONEMPTY_VALUES)
@checkers.test
def test_assert_not_empty_ok(collection):
  asserts.is_not_empty(collection)


@checkers.parameterize(EMPTY_VALUES)
@checkers.test
def test_assert_not_empty_bad(collection):
  with asserts.expect_exception(AssertionError):
    asserts.is_not_empty(collection)


@checkers.test
def test_assert_none_ok():
  asserts.is_none(None)


@checkers.test
def test_assert_none_bad():
  with asserts.expect_exception(AssertionError):
    asserts.is_none(0)


@checkers.test
def test_assert_not_none_ok():
  asserts.is_not_none(False)


@checkers.test
def test_assert_not_none_bad():
  with asserts.expect_exception(AssertionError):
    asserts.is_not_none(None)


@checkers.parameterize(TRUTHY_VALUES)
@checkers.test
def test_assert_same_ok(value):
  asserts.are_same(value, value)


@checkers.parameterize(DIFFERENT_INSTANCE_VALUES)
@checkers.test
def test_assert_same_bad(x, y):
  with asserts.expect_exception(AssertionError):
    asserts.are_same(x, y)


@checkers.parameterize(DIFFERENT_INSTANCE_VALUES)
@checkers.test
def test_assert_not_same_ok(x, y):
  asserts.are_not_same(x, y)


@checkers.parameterize(TRUTHY_VALUES)
@checkers.test
def test_assert_not_same_bad(value):
  with asserts.expect_exception(AssertionError):
    asserts.are_not_same(value, value)


@checkers.parameterize(EMPTY_VALUES)
@checkers.parameterize(NONEMPTY_VALUES)
@checkers.test
def test_assert_length_ok(collection, length):
  asserts.has_length(collection, length)


@checkers.parameterize(EMPTY_VALUES)
@checkers.test
def test_assert_length_bad(collection):
  with asserts.expect_exception(AssertionError):
    asserts.has_length(collection, 1)


if __name__ == '__main__':
  pyunit.main()

