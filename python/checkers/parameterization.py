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

"""Defines mechanism for defining parameterizations for a test."""

import registry


class Parameterization(object):
  """Parameterizations hold the values to fully instantiate a test case.

  Parameterizations only come in useful when doing data-driven testing. If a
  test is defined with open variables that need to be assigned outside of the
  initial declaration (and isn't something assigned at the test run's level),
  then that should be done through a parameterization.

  For example, say a test is defined as follows:
    @checkers.test
    def test_add(calculator, x, y, z):
      total = calculator.add(x, y)
      asserts.are_equal(z, total,
                        'expected %s + %s == %s; got %s' % (x, y, z, total))

  Generally, the calculator would be a component registered with the test run,
  and x, y, and z would be test case-specific values assigned via the test's
  parameterization.
  """

  def __init__(self, name, variables=None):
    """Initializes a new instance of a Parameterization.

    Note that the name provided for the parameterization must be usable as the
    suffix for a Python identiier (numbers, letters, and _ only). This will be
    appended to the original test's name. (e.g. if the name is '2_4_6', then
    the test_add function above would have a paramterized name of
    test_add_2_4_6).

    The variables argument can be any sort of dict-like object that holds
    variables, like a VariableRegistry. It will be converted to an actual
    variable registry here.

    Args:
      name: (string) Name for the parameterization (also suffix for test case).
      variables: (Registry): Values to apply in the parameterization.
    """
    self.name = name
    self.variables = registry.Registry()
    self.suites = set()
    if variables:
      for key, value in variables.iteritems():
        if key == 'test_suites':
          for name in value:
            self.suites.add(name)
        self.variables.register(key, value)

