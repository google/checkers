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

"""Example of a very simple test of the 'hello world' variety."""

import checkers
from checkers import asserts
from checkers.runners import pyunit


@checkers.test
def test_hello_world():
  """Simple test that asserts that the hello string is not empty."""
  hello = 'hello, world'
  asserts.is_not_empty(hello)


if __name__ == '__main__':
  pyunit.main()

