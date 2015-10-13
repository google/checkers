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

"""Test suites are used for grouping Checkers tests.

Note that suites are managed at the Test level, not the TestCase level. So if a
test will become multiple test cases, then all of those test cases will be in
the original test's suite.
"""

import modules
import registry


class TestSuite(registry.AutoKeyRegistry):
  """A TestSuite is basically just a collection of tests.

  It is a little smarter than a normal TestRegistry because when a new test is
  added to a test suite, we also need to make sure that it is added to the test
  run as well.
  """

  @staticmethod
  def from_module(module, name=None):
    """Creates a new test suite out of all of the tests in a module.

    Args:
      module: (module) The module to load the tests from.
      name: (string) The name of the test suite (defaults to module short name).

    Returns:
      TestSuite: The test suite containing the tests from the module.
    """
    name = name if name else modules.find_module_name(module, False)
    description = None
    if hasattr(module, '__doc__'):
      description = module.__doc__
    suite = TestSuite(name, description=description)
    for test in modules.tests_from_module(module).values():
      suite.register(test)
    return suite

  def __init__(self, name, description=None):
    """Initializes a new instance of a TestSuite.

    Args:
      name: (string) The name of the test suite.
      description: (string) A description of the test suite.
    """
    super(TestSuite, self).__init__(lambda test: test.full_name)
    self.name = name
    self.description = description if description else 'No description.'
    self._test_run = None

  @property
  def test_run(self):
    """Gets the test run."""
    return self._test_run

  @test_run.setter
  def test_run(self, test_run):
    """Sets the test run.

    It will also make sure all of the test cases in the suite are registered
    with the test run.

    Args:
      test_run: (TestRun) The test run to add to the test suite.
    """
    self._test_run = test_run
    for test in self.values():
      self.test_run.tests.register(test)

  def register(self, test):
    """Adds a test to the test suite.

    Args:
      test: (Test) The test to add.
    """
    super(TestSuite, self).register(test)
    if self.test_run:
      self.test_run.tests.register(test)

