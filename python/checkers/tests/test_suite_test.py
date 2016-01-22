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

"""Tests for checkers.test_suite."""

import sys

import checkers
from checkers import asserts
from checkers import test_run
from checkers import test_suite
from checkers.runners import pyunit


@checkers.test
def test_test_suite_from_module():
  module = sys.modules[__name__]
  suite = test_suite.TestSuite.from_module(module)
  asserts.is_not_empty(suite)
  asserts.are_equal(suite.name, 'test_suite_test')


@checkers.test
def test_test_suite_init():
  ts = test_suite.TestSuite('foo', 'foo description')
  asserts.are_equal(ts.name, 'foo')
  asserts.are_equal(ts.description, 'foo description')
  asserts.is_none(ts.test_run)


@checkers.test
def test_test_suite_test_run():
  ts = test_suite.TestSuite('foo')
  ts.register(test_test_suite_from_module)
  ts.test_run = test_run.TestRun('Foo')
  asserts.is_not_none(ts.test_run)
  asserts.is_in(test_test_suite_from_module.full_name, ts.test_run.tests)


if __name__ == '__main__':
  pyunit.main()

