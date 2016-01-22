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

"""Tests for the checkers package (__init__.py file)."""

import checkers
from checkers import asserts
from checkers.runners import pyunit


@checkers.test
def test_teardown_decorator():
  """Test that the teardown decorator works properly."""

  def teardown_func1():
    pass

  def teardown_func2():
    pass

  @checkers.teardown(teardown_func1, teardown_func2)
  @checkers.test
  def test_sample_for_teardown():
    pass

  asserts.is_in(teardown_func1.__name__, test_sample_for_teardown.teardown)
  asserts.is_in(teardown_func2.__name__, test_sample_for_teardown.teardown)


@checkers.test
def test_setup_decorator():
  """Test that the setup decorator works properly."""

  def setup_func1():
    pass

  def setup_func2():
    pass

  @checkers.setup(setup_func1, setup_func2)
  @checkers.test
  def test_sample_for_setup():
    pass

  asserts.is_in(setup_func1.__name__, test_sample_for_setup.setup)
  asserts.is_in(setup_func2.__name__, test_sample_for_setup.setup)


@checkers.test
def test_suites_decorator():
  """Tests that the test_suites decorator applies suite names properly."""

  @checkers.test_suites('suite1', 'suite2')
  @checkers.test
  def test_sample_for_suites():
    pass

  asserts.is_in('suite1', test_sample_for_suites.test_suite_names)
  asserts.is_in('suite2', test_sample_for_suites.test_suite_names)


@checkers.test
def test_parameterize_decorator():
  """Tests that the parameterize decorator sets parameterizations properly."""

  @checkers.parameterize({
      'foo': {'x': 0},
      'bar': {'x': 1},
  })
  @checkers.test
  def test_sample_for_parameterize():
    pass
  asserts.is_in('foo', test_sample_for_parameterize.decorator_parameterizations)
  asserts.is_in('bar', test_sample_for_parameterize.decorator_parameterizations)


if __name__ == '__main__':
  pyunit.main()

