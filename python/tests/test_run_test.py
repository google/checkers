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

"""Tests for checkers.test_run."""

import sys

import checkers
from checkers import asserts
from checkers import test_run
from checkers.runners import pyunit


@checkers.test
def test_test_run_from_module():
  module = sys.modules[__name__]
  run = test_run.TestRun.from_module(module)
  asserts.is_not_empty(run.tests)
  asserts.are_equal(run.name, 'test_run_test')


@checkers.test
def test_test_run_init():
  run = test_run.TestRun('foo')
  asserts.are_equal(run.name, 'foo')
  asserts.is_empty(run.variables)
  asserts.is_empty(run.setup)
  asserts.is_empty(run.teardown)
  asserts.is_empty(run.test_case_setup)
  asserts.is_empty(run.test_case_teardown)
  asserts.is_empty(run.test_suites)
  asserts.is_empty(run.parameterizations)


if __name__ == '__main__':
  pyunit.main()

