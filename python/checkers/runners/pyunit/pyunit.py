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

"""Module that allows Checkers tests to be used with PyUnit test runner.

This also provides a main function that calls a PyUnit-based main function once
the Checkers tests have been "discovered" by PyUnit.

Note that the way this works, Checkers will go ahead and run all of the tests in
the Checkers test runs. It then converts those test results into PyUnit test
suites. So the PyUnit test runner doesn't actually re-run the tests. Rather, it
uses the exception info in the test results to re-raise any exceptions that may
have been raised in the original run. Why go through all this, you ask? Well,
this allows us to place a test case into multiple test suites without running
tests multiple times. It also gives us some control over sharding should the
need arise someday.

Note: PyUnit is now the unittest module, but it's easier to use PyUnit as the
general notion of tests structured to use unittest.

Note: Since we're still using the PyUnit-based main method, the existing PyUnit
tests will be included by default in the test results. So there is no danger in
porting your existing unittest.main function over to just pyunit.main. That way
you can add both PyUnit-based tests and Checkers tests.

Example:

class FooTest(unittest.TestCase):

  def test_foo(self):
    self.assert_true(True)

@checkers.test
def test_bar():
  self.assert_true(True)

# This will run both FooTest and test_bar.

if __name__ == '__main__':
  pyunit.main()

"""

import sys
import traceback
import unittest

import checkers

def run_test_run(test_run):
  """Runs all of the tests in the test run and returns the results in suites.

  This function returns a registry that is keyed by the test suite names, and
  then under each suite is a TestResultRegistry containing all of the test
  results for that test suite.

  Args:
    test_run: (TestRun) The test run containing the tests to be run.

  Returns:
    Registry(suite_name, TestResultRegistry)
  """
  # Run all of the tests and get the test results.
  results = checkers.Registry()
  for setup in test_run.setup.values():
    setup(test_run)
  for test_case in test_run.generate_test_cases.values():
    if test_case.full_name not in results:
      results[test_case.full_name] = test_case()
    result = results[test_case.full_name]
  for teardown in test_run.teardown.values():
    teardown(test_run)

  # Group all of the test results by their test suites.
  suites = checkers.Registry()
  for result in results.values():
    for suite in result.context.test_case.test_suites.values():
      suite_name = test_run.name
      if suite.name:
        suite_name = '%s.%s' % (test_run.name, suite.name)
      if suite_name not in suites:
        suites.register(suite_name, checkers.AutoKeyRegistry(
            lambda tr: tr.context.test_case.full_name))
      suites[suite_name].register(result)
  return suites


def create_pyunit_test_method(result):
  """Creates a test method to be added to the PyUnit TestCase class.

  Args:
    result: (TestResult) The result from running the test.

  Returns:
    function: The method that will be added to the PyUnit TestCase class.
  """

  def pyunit_test_method(_):
    """The actual method that should be added to the PyUnit TestCase class.

    The argument passed in is the class instance (self), but Checkers tests do
    not know or care about the PyUnit test, so that argument is ignored. In
    fact, all that happens in this function is we take the test result from the
    previously-run checkers test and, if it failed (raised an exception), we
    re-raise it as if it had just happened. This is to trick PyUnit into
    thinking it just ran a test. :P
    """
    if result.exc_info:
      raise result.exc_info[1], None, result.exc_info[2]

  test_method = pyunit_test_method
  test_method.func_name = str(result.context.test_case.name)
  if not test_method.func_name.startswith('test'):
    test_method.func_name = 'test_%s' % test_method.func_name
  test_method.func_doc = result.context.test_case.description
  return test_method


def create_pyunit_test_suite(parent_module_name, suite_name, test_run,
                             test_results, test_suite_type):
  """Creates a PyUnit TestCase class from a Checkers test suite.

  Remember that in PyUnit-land, a TestCase class is really a test suite, so the
  naming in this file can be a bit confusing, but hopefully it is consistent.

  Args:
    parent_module_name: (string) Name of the module to put the generated tests.
    suite_name: (string) Name of the test suite where the test should be stored.
    test_run: (TestRun) Test run that was responsible for running the test.
    test_results: (TestResultRegistry) Set of test results for the test suite.
    test_suite_type: (type) Base type for the generated PyUnit test cases.

  Returns:
    A unittest.TestCase class containing the test functions for the suite.
  """
  test_class_attrs = {}
  for result in test_results.values():
    test_name = result.context.test_case.name
    test_class_attrs[test_name] = create_pyunit_test_method(result)
  test_class_attrs['test_run'] = test_run
  cls_name = suite_name
  cls = type(cls_name, (test_suite_type,), test_class_attrs)
  cls.__module__ = parent_module_name
  return cls


def create_pyunit_test_suites(module, checkers_test_runs, checkers_test_results,
                              test_suite_type, pyunit_discovered_tests=None):
  """Creates a PyUnit TestSuite that contains all of the real test suites.

  Note on terminiology: in the unittest module, all of the tests and test suites
  go into a single major test suite. This function creates the overall container
  master test suite. Within this test suite are the tests that were discovered
  by PyUnit (assuming you chose to include those) as well as all of the Checkers
  test suites.

  Args:
    module: (module) Module where the generated test suites should be placed.
    checkers_test_runs: ([TestRun]) Set of Checkers test runs to execute.
    checkers_test_results: (Registry(str, TestResultRegistry)) See run_test_run.
    test_suite_type: (type) Base type for the generated PyUnit test cases.
    pyunit_discovered_tests: (unittest.TestSuite): Previously-discovered tests.

  Returns:
    unittest.TestSuite containing *all* of the tests, both PyUnit and Checkers.
  """
  pyunit_suite = unittest.TestSuite()
  if pyunit_discovered_tests:
    pyunit_suite.addTest(pyunit_discovered_tests)

  loader = unittest.defaultTestLoader
  for run in checkers_test_runs:
    result_suites = checkers_test_results[run.name]
    for suite_name, results  in result_suites.iteritems():
      pyunit_test_suite = create_pyunit_test_suite(
          module.__name__, suite_name, run, results, test_suite_type)
      pyunit_suite.addTest(loader.loadTestsFromTestCase(pyunit_test_suite))
  return pyunit_suite


def load_checkers_tests(module, test_runs, checkers_test_results,
                        test_suite_type, include_pyunit_tests):
  """Load Checkers tests so that they'll be discoverable by PyUnit.

  Using the load_tests protocol, this will register a load_tests function in the
  provided module so that PyUnit will be able to discover the Checkers tests.

  Args:
    module: (module) Module where the generated test suites should be placed.
    test_runs: ([TestRun]) Set of Checkers test runs to execute.
    checkers_test_results: (Registry(str, TestResultRegistry)) See run_test_run.
    test_suite_type: (type) Base type for the generated PyUnit test cases.
    include_pyunit_tests: (bool): Include any discovered PyUnit-based tests.
  """
  # TODO(barkimedes): If there is an existing load_tests function, call it.
  def pyunit_load_tests(loader, tests, pattern):  # pylint: disable=unused-argument, g-line-too-long
    if not include_pyunit_tests:
      tests = unittest.TestSuite()
    result = None
    try:
      result = create_pyunit_test_suites(
          module, test_runs, checkers_test_results, test_suite_type, tests)
    except:
      traceback.print_exc()
      raise
    return result
  setattr(module, 'load_tests', pyunit_load_tests)


def main(test_runs=None, test_run=None, module=None,
         include_pyunit_tests=True, main_module=unittest,
         test_suite_type=unittest.TestCase,
         *args, **kwargs):
  """Main function that will run both Checkers and PyUnit tests.

  Args:
    test_runs: ([TestRun]) Set of Checkers test runs to execute.
    test_run: (TestRun) A single Checkers test run to execute.
    module: (module) Module where the generated test suites should be placed.
    include_pyunit_tests: (bool): Include any discovered PyUnit-based tests.
    main_module: (module) Module that defines the PyUnit main method to use.
    test_suite_type: (type) Base type for the generated PyUnit test cases.
    *args: (tuple) Positional arguments to pass through to the real main.
    **kwargs: (dict) Keyword arguments to pass through to the real main.

  Returns:
    Whatever the PyUnit main's function returns.
  """
  if not module:
    module = sys.modules['__main__']
  if not test_runs:
    test_runs = []
  if test_run:
    test_runs.append(test_run)
  if not test_runs:
    test_run = checkers.TestRun.from_module(module)
    test_runs.append(test_run)
  checkers_results = {}
  for run in test_runs:
    checkers_results[run.name] = run_test_run(run)

  # Load the test results into the PyUnit test suites for discovery.
  load_checkers_tests(module, test_runs, checkers_results,
                      test_suite_type=test_suite_type,
                      include_pyunit_tests=include_pyunit_tests)
  return main_module.main(*args, **kwargs)

