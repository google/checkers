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

"""Context provides environmental information for a test."""

import registry


class Context(object):
  """Context provides environmental information to a test.

  Note that a unique context will be created for each test case, so any changes
  that you make to the context will only affect its associated test. That
  being said, the context will make a shallow copy of variables registered with
  the test run, so any changes that you make to any of those variables will be
  reflected in other tests.

  Your best bet is to register any "global" dependencies with the test run. For
  any dependencies specific to a test, register them directly with the context
  (this can be done in a test's setup function).
  """

  def __init__(self, test_case, test_run, **variables):
    """Initializes a new instance of a Context.

    The variables arg can be a dict, but it can also be an existing variable
    registry since it behaves like a variable dict.

    Args:
      test_case: (TestCase) The test case that the context is associated with.
      test_run: (TestRun) The test run that contains the test.
      **variables: (dict) Variables that need to be passed through to the test.
    """
    # The test case associated with the context
    self.test_case = test_case
    # The test run that owns/controls the test.
    self.test_run = test_run
    # Set of variables available for the test.
    self.variables = registry.Registry()
    for key, value in variables.iteritems():
      self.variables.register(key, value)
    # Of course, the context itself must be available to tests.
    self.variables.register('context', self)

