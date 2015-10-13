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

"""Module defining a test run which is responsible for managing tests."""

import sys

import context
import modules
import registry
import test_suite


class _TestRunSuiteRegistry(registry.AutoKeyRegistry):
  """Registry that contains the test suites for a test run."""

  def __init__(self, test_run):
    """Registry that contains the test suites for a given test run.

    Args:
      test_run: (TestRun) The test run that the suites will belong to.
    """
    super(_TestRunSuiteRegistry, self).__init__(lambda ts: ts.name)
    self.test_run = test_run

  def __getitem__(self, suite_name):
    """Gets the item with the given key from the registry."""
    if suite_name not in self._values:
      self._values[suite_name] = test_suite.TestSuite(suite_name)
    return self._values[suite_name]

  def register(self, suite):
    """Registers the test suite, but also sets the test_run for the suite.

    Args:
      suite: (TestSuite) The test suite being registered.
    """
    super(_TestRunSuiteRegistry, self).register(suite)
    suite.test_run = self.test_run


class TestRun(object):
  """Test run is a set of tests that need to be run and their shared context."""

  @staticmethod
  def from_module(module=None, module_name=None):
    """Creates a new test run out of all of the tests in a module.

    If module is provided, then that module is used. Otherwise, if module_name
    is defined, then we try to find the module with that name and use that.
    If neither one is provided, then we find the module named '__main__'.

    Args:
      module: (module) The module to load the tests from.
      module_name: (string) The name of the module to load the tests from.

    Returns:
      TestRun: The test run containing the tests from the module.
    """
    if not module_name:
      module_name = '__main__'
    if not module:
      module = sys.modules[module_name]
    test_run = TestRun(modules.find_module_name(module))
    tests = modules.tests_from_module(module)
    for test in tests.values():
      test_run.tests.register(test)
    return test_run

  def __init__(self, name):
    """Initializes a new instance of a TestRun.

    Args:
      name: (string) The name to use for the test run.
    """
    self.name = name
    self.tests = registry.AutoKeyRegistry(lambda test: test.full_name)
    self.variables = registry.Registry()
    self.setup = registry.AutoKeyRegistry(lambda func: func.__name__)
    self.teardown = registry.AutoKeyRegistry(lambda func: func.__name__)
    self.test_case_setup = registry.AutoKeyRegistry(lambda func: func.__name__)
    self.test_case_teardown = registry.AutoKeyRegistry(
        lambda func: func.__name__)
    self.test_suites = _TestRunSuiteRegistry(self)
    # Parameterizations are stored with the key as the test's full name and the
    # value is a parameterization registry.
    param_key = lambda param: param.name
    # pylint: disable=line-too-long
    parameterization_registry_factory = lambda: registry.AutoKeyRegistry(param_key)
    # pylint: enable=line-too-long
    self.parameterizations = registry.SuperRegistry(
        parameterization_registry_factory)

  @property
  def generate_test_cases(self, context_factory=context.Context):
    """Generates the real test cases for the test run.

    A test case is essentially the closure of a test. So what this function does
    is take all of the tests that have been defined, creates test cases for
    them, and (for each test case), sets up what test suites it is a member of.
    It also adds all of the variables from the test run to each test case's
    individual context.

    All tests will be added to a global test suite.

    Args:
      context_factory: (function(test_case, test_run)) Creates a context.

    Returns:
      TestCaseRegistry: Registry containing all of the test cases for the run.
    """
    global_suite = test_suite.TestSuite('all', 'Suite containing all tests.')
    test_case_registry = registry.AutoKeyRegistry(lambda tc: tc.full_name)
    for original_test in self.tests.values():
      test = original_test.clone()
      # Add all of the parameterizations just on the test to the test in the
      # test run.
      for parameterization in test.decorator_parameterizations.values():
        self.parameterizations.register(test.full_name, parameterization)
      # Make sure that the decorator setup functions are called closer to the
      # test than the test run's test case setup functions.
      test.setup.clear()
      test.setup.merge(self.test_case_setup)
      test.setup.merge(original_test.setup)
      test.teardown.merge(self.test_case_teardown)
      for suite_name in test.test_suite_names:
        self.test_suites[suite_name].register(test)
      new_context_factory = lambda test_case: context_factory(test_case, self)
      params = None
      if test.full_name in self.parameterizations:
        params = self.parameterizations[test.full_name]
      test_cases = test.generate_test_cases(new_context_factory, params)
      for test_case in test_cases.values():
        # Replace the empty suite provided by parameterizations with the actual
        # suite from the test run.
        for suite_name in test_case.test_suites:
          self.test_suites[suite_name].register(test_case)
          test_case.test_suites.register(self.test_suites[suite_name])
        test_case.test_suites.register(global_suite)
        for suite in self.test_suites.values():
          if test.full_name in suite or test_case.full_name in suite:
            test_case.test_suites.register(suite)
        test_case_registry.register(test_case)
        for key, value in self.variables.iteritems():
          test_case.context.variables.register(key, value)
    return test_case_registry

