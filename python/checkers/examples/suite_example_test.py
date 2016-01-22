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

"""Example of various mechanisms for organizing tests into test suites."""

import checkers
from checkers import asserts
from checkers.examples import subtraction_tests
from checkers.runners import pyunit


@checkers.test_suites('addition', 'multiplication')
@checkers.parameterize({
    '0_0': {'x': 0, 'expected': 0, 'test_suites': ['identity']},
    '1_2': {'x': 1, 'expected': 2},
    '4_8': {'x': 4, 'expected': 8},
    'n2_n4': {'x': -2, 'expected': -4},
})
@checkers.test
def test_double(x, expected):
  asserts.are_equal(x + x, expected)
  asserts.are_equal(x * 2, expected)


@checkers.parameterize({
    '0_1_1': {'x': 0, 'y': 1, 'expected': 1, 'test_suites': ['identity']},
    '1_2_3': {'x': 1, 'y': 2, 'expected': 3},
    '4_8_12': {'x': 4, 'y': 8, 'expected': 12},
})
@checkers.test
def test_add(x, y, expected):
  asserts.are_equal(x + y, expected)


def create_test_run():
  test_run = checkers.TestRun.from_module()
  test_run.test_suites['addition'].register(test_add)
  subtraction_suite = checkers.TestSuite.from_module(subtraction_tests)
  test_run.test_suites.register(subtraction_suite)
  return test_run

if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())

