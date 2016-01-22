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

"""Tests for checkers.test_case."""

import checkers
from checkers import asserts
from checkers import test_case
from checkers import test_result
from checkers.runners import pyunit


def _dummy_context_factory(tc):
  return checkers.Context(tc, None)


@checkers.test
def _dummy_test():
  pass


@checkers.test
def test_test_case_init():
  test = _dummy_test
  context_factory = _dummy_context_factory
  tc = test_case.TestCase(test, context_factory)
  asserts.are_equal(tc.name, '_dummy_test')
  asserts.are_equal(tc.full_name, 'test_case_test._dummy_test')
  asserts.are_same(tc.test, test)
  asserts.is_not_none(tc.context)
  asserts.is_empty(tc.description)
  asserts.is_empty(tc.test_suites)


@checkers.test
def test_test_call_fixtures():
  tracker = set()

  def foo_setup():
    tracker.add('foo_setup')

  def bar_setup(context):
    if context:
      tracker.add('bar_setup')

  def foo_teardown():
    tracker.add('foo_teardown')

  def bar_teardown(context):
    if context:
      tracker.add('bar_teardown')

  @checkers.setup(foo_setup, bar_setup)
  @checkers.teardown(foo_teardown, bar_teardown)
  @checkers.test
  def dummy_test():
    tracker.add('dummy_test')

  context_factory = _dummy_context_factory
  tc = test_case.TestCase(dummy_test, context_factory)
  result = tc()
  asserts.are_equal(result.status, test_result.TestResultStatus.PASSED)
  asserts.has_length(tracker, 5)


@checkers.test
def test_test_call_failure_from_assertion():
  @checkers.test
  def dummy_test():
    asserts.is_true(False)

  context_factory = _dummy_context_factory
  tc = test_case.TestCase(dummy_test, context_factory)
  result = tc()
  asserts.are_equal(result.status, test_result.TestResultStatus.FAILED)


@checkers.test
def test_test_call_error_from_exception():
  @checkers.test
  def dummy_test():
    raise ValueError('just raising a random exception...')

  context_factory = _dummy_context_factory
  tc = test_case.TestCase(dummy_test, context_factory)
  result = tc()
  asserts.are_equal(result.status, test_result.TestResultStatus.ERROR)


if __name__ == '__main__':
  pyunit.main()

