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

"""Example of how to use parameterizations to pass in test data."""

import checkers
from checkers import asserts
from checkers.examples.calculator import Calculator
from checkers.runners import pyunit


# In this example, the parameterization is applied directly to the test method.
# That means that these parameterizations will always be applied whenever this
# test is used in a test run. Use with caution!
@checkers.parameterize({
    '8_2_6': {'x': 8, 'y': 2, 'expected': 6},
    '0_1_n1': {'x': 0, 'y': 1, 'expected': -1},
})
@checkers.test
def test_subtract(calculator, x, y, expected):
  asserts.are_equal(calculator.subtract(x, y), expected)
  print '%d - %d = %d' % (x, y, expected)


@checkers.test
def test_add(calculator, x, y, expected):
  asserts.are_equal(calculator.add(x, y), expected)
  print '%d + %d = %d' % (x, y, expected)


# Since the parameterizations are defined in a function, you can imagine using
# this in a wide variety of scenarios. For example, you could have code here
# that parses test data from a data file or grabs it from a datastore of some
# sort. This provides a built-in, flexible parameterization.
def build_add_params():
  """Function that creates a set of Parameerizations for the add test.

  Returns:
    List of initialized Parameterization instances.
  """
  return [
      checkers.Parameterization('1_1_2', {'x': 1, 'y': 1, 'expected': 2}),
      checkers.Parameterization('2_2_4', {'x': 2, 'y': 2, 'expected': 4}),
      checkers.Parameterization('4_8_12', {'x': 4, 'y': 8, 'expected': 12}),
      checkers.Parameterization('2_n1_1', {'x': 2, 'y': -1, 'expected': 1}),
  ]


def create_test_run():
  test_run = checkers.TestRun.from_module()
  test_run.variables.register('calculator', Calculator())
  # The parameterizations are applied at the test run level, so they only apply
  # to this test run.
  # You should prefer this mechanism for creating parameterizations that may be
  # dependent on the environment, that you have to load data from another
  # location (like a database), or where the components under test may behave
  # differently from each other so the parameters would have to change between
  # test runs.
  for param in build_add_params():
    test_run.parameterizations.register(test_add.full_name, param)
  return test_run


if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())

