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

"""Detailed example of a very simple test of the 'hello world' variety."""

import checkers
from checkers import asserts
from checkers.runners import pyunit


@checkers.test
def test_hello_world():
  """Simple test that asserts that the hello string is not empty."""
  hello = 'hello, world'
  asserts.is_not_empty(hello)


def create_test_run():
  # You can create a test run directly and then register individual tests.
  test_run = checkers.TestRun('hello')
  test_run.tests.register(test_hello_world)

  # Alternatively, you could also create a test run from the module.
  # (This is the default behavior of pyunit.main when no test run is specified.)
  # module = sys.modules[__name__]
  # test_run = checkers.TestRun.from_module(module)
  return test_run


if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())

