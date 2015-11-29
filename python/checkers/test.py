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

"""Module defining the concept of a test, which represents a test's steps."""

import inspect

import modules
import registry
from test_case import TestCase
from test_suite import TestSuite


class Test(object):
  """Test is a base class that represents a test case or a test template."""

  def __init__(self, name, full_name, description):
    """Initializes a new instance of a test.

    Args:
      name: (string) The name of the test.
      full_name: (string) The fully-qualified name of the test.
      description: (string) A description of the test.
    """
    self.name = unicode(name)
    self.full_name = unicode(full_name)
    self.description = unicode(description)
    self.decorator_parameterizations = registry.AutoKeyRegistry(
        lambda param: param.name)
    self.setup = registry.AutoKeyRegistry(lambda func: func.__name__)
    self.teardown = registry.AutoKeyRegistry(lambda func: func.__name__)
    self.test_suite_names = set()

  def clone(self):
    """Creates a shallow copy of the test.

    Returns:
      Test: A shallow copy of this test instance.
    """
    test = Test(self.name, self.full_name, self.description)
    test.decorator_parameterizations.merge(self.decorator_parameterizations)
    test.setup.merge(self.setup)
    test.teardown.merge(self.teardown)
    test.test_suite_names |= self.test_suite_names
    return test

  def __call__(self):
    """Executes the actual test."""
    raise NotImplementedError('The subclass must implement this method.')

  @property
  def required_variables(self):
    """Gets the set of variables required to run the test."""
    raise NotImplementedError('The subclass must implement this method.')

  def generate_test_cases(self, context_factory, parameterizations=None):
    """Creates the set of test cases that this test represents.

    The parameterizations argument should contain a parameterizations registry
    (keyed by parameterization name) containing values that are instances of
    a checkers.Parameterization class.

    Args:
      context_factory: Callable to create a context instance given a TestCase.
      parameterizations: (Registry) Parameterizations used to create test cases.

    Returns:
      list(TestCase): List of test cases (aka test closures).
    """
    test_cases = registry.AutoKeyRegistry(lambda tc: tc.full_name)
    if not parameterizations:
      test_case = TestCase(self, context_factory,
                           description=self.description)
      test_cases.register(test_case)
      return test_cases
    # It is a parameterized test, so we need to generate multiple test cases;
    # one for each parameterization.
    for suffix, param in parameterizations.iteritems():
      name = '%s_%s' % (self.name, suffix)
      full_name = '%s_%s' % (self.full_name, suffix)
      test_case = TestCase(self, context_factory, name=name,
                           full_name=full_name, description=self.description)
      for key, value in param.variables.iteritems():
        test_case.context.variables.register(key, value)
      for suite_name in param.suites:
        test_case.test_suites.register(TestSuite(suite_name))
      test_cases.register(test_case)
    return test_cases


class FunctionTest(Test):
  """Provides an adaptor to convert a function into a Test instance."""

  def __init__(self, test_function):
    """Initializes a new instance of a FunctionTest.

    Args:
      test_function: (callable) The function that the test is wrapping.
    """
    name = test_function.func_name
    full_name = '%s.%s' % (
        modules.find_module_name_from_name(test_function.__module__),
        test_function.func_name)
    description = test_function.func_doc
    super(FunctionTest, self).__init__(name, full_name, description)
    self.function = test_function

  def clone(self):
    """Creates a shallow copy of the test.

    Returns:
      Test: A shallow copy of this test instance.
    """
    test = FunctionTest(self.function)
    test.decorator_parameterizations.merge(self.decorator_parameterizations)
    test.setup.merge(self.setup)
    test.teardown.merge(self.teardown)
    test.test_suite_names |= self.test_suite_names
    return test

  def __call__(self, *args, **kwargs):
    """Allows users to call the test like the original function.

    Args:
      *args: (tuple) Positional args to pass to the underlying function.
      **kwargs: (dict) Keyword args to pass to the underlying function.

    Returns:
      Whatever the original function would have returned.
    """
    return self.function(*args, **kwargs)

  @property
  def required_variables(self):
    """Gets the set of variables required to actually call the function."""
    argspec = inspect.getargspec(self.function)
    if not argspec.defaults:
      return argspec.args
    return argspec.args[:-len(argspec.defaults)]

