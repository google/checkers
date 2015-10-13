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

"""Module defining the concept of a test case, which is an individual test.

Think of a test case as being the closure of a test where the variables have
been applied. A test case's __call__ function does not take any arguments.
"""

import inspect
import sys

import registry
import test_result


class TestCase(object):
  """TestCase represents an individual test case that tests a single concept."""

  def __init__(self, test, context_factory, name=None, full_name=None,
               description=''):
    """Initializes a new instance of a TestCase.

    Args:
      test: (Test) The test that the test case provides closure for.
      context_factory: (function(test_case)) Function that creates a context.
      name: (string) The name of the test case.
      full_name: (string) The fully-qualified name of the test case.
      description: (string) A description of the test case.
    """
    self.name = name if name else test.name
    self.full_name = full_name
    if not full_name:
      self.full_name = test.full_name
    self.test = test
    self.context = context_factory(self)
    self.description = description
    self.test_suites = registry.AutoKeyRegistry(lambda suite: suite.name)

  def __call__(self):
    """Executes the checkers test (including setup/teardown methods).

    Note that implementing classes should use this to actually execute the test.

    Returns:
      TestResult: The result of running the test case.
    """
    exception = None
    exc_info = None
    try:
      for setup in self.test.setup.values():
        if inspect.getargspec(setup).args:
          setup(self.context)
        else:
          setup()
      # TODO(barkimedes): support tests with args.
      args = {}
      for variable in self.test.required_variables:
        args[variable] = self.context.variables[variable]
      self.test(**args)
    except Exception as ex:  # pylint: disable=broad-except
      exception = ex
      exc_info = sys.exc_info()
    finally:
      for teardown in self.test.teardown.values():
        try:
          if inspect.getargspec(teardown).args:
            teardown(self.context)
          else:
            teardown()
        except Exception as ex:  # pylint: disable=broad-except
          if not exception:
            exception = ex
            exc_info = sys.exc_info()
    if exception:
      if isinstance(exception, AssertionError):
        return test_result.TestResult(
            self.context, test_result.TestResultStatus.FAILED,
            exc_info=exc_info)
      return test_result.TestResult(
          self.context, test_result.TestResultStatus.ERROR, exc_info=exc_info)
    return test_result.TestResult(self.context,
                                  test_result.TestResultStatus.PASSED)

