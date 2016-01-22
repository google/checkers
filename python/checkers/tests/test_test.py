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

"""Tests for checkers.test."""

import checkers
from checkers import asserts
from checkers import Test
from checkers.runners import pyunit


@checkers.test
def test_test_init():
  t = Test('foo', 'bar.foo', 'foo bar test')
  asserts.are_equal(t.name, 'foo')
  asserts.are_equal(t.full_name, 'bar.foo')
  asserts.are_equal(t.description, 'foo bar test')
  asserts.is_empty(t.decorator_parameterizations)
  asserts.is_empty(t.setup)
  asserts.is_empty(t.teardown)
  asserts.is_empty(t.test_suite_names)


@checkers.test
def test_test_clone():
  original = Test('foo', 'bar.foo', 'foo bar test')
  clone = original.clone()
  asserts.are_equal(clone.name, 'foo')
  asserts.are_equal(clone.full_name, 'bar.foo')
  asserts.are_equal(clone.description, 'foo bar test')
  asserts.is_empty(clone.decorator_parameterizations)
  asserts.is_empty(clone.setup)
  asserts.is_empty(clone.teardown)
  asserts.is_empty(clone.test_suite_names)


@checkers.test
def test_test_call_not_implemented():
  t = Test('foo', 'bar.foo', 'foo bar test')
  with asserts.expect_exception(NotImplementedError):
    t()

@checkers.test
def test_test_required_variables_not_implemented():
  t = Test('foo', 'bar.foo', 'foo bar test')
  with asserts.expect_exception(NotImplementedError):
    t.required_variables()


# TODO(barkimedes): Add tests for generate_test_cases, but for now it's
# fairly well covered by the tests in the examples and tests directories..


if __name__ == '__main__':
  pyunit.main()

