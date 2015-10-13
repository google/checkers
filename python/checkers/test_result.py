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

"""Contains the TestResult class which stores results from a Checkers test."""


def enum(**enums):
  """Converts the provided key/value pairs into enumerations."""
  return type('Enum', (), enums)

TestResultStatus = enum(
    PASSED='PASSED',
    FAILED='FAILED',
    ERROR='ERROR'
)


class TestResult(object):
  """A TestResult stores information about the result of a test."""

  def __init__(self, context, status, message='', exc_info=None):
    """Initializes a new instance of a TestResult.

    Args:
      context: (Context) The context of the test case that produced the result.
      status: (TestResultStatus (string)) The current status of the test.
      message: (string) The [error] message for the test.
      exc_info: See https://docs.python.org/2/library/sys.html#sys.exc_info.
    """
    self.context = context
    self.status = status
    self.message = message
    self.exc_info = exc_info
    if not self.message and self.exc_info:
      self.message = str(self.exc_info[1])

