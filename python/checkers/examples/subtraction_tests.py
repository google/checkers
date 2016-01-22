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

"""Module containing some subtraction tests (demo purposes only)."""

import checkers
from checkers import asserts


@checkers.parameterize({
    '8_2_6': {'x': 8, 'y': 2, 'expected': 6},
    '0_1_n1': {'x': 0, 'y': 1, 'expected': -1},
})
@checkers.test
def test_subtract(x, y, expected):
  return asserts.are_equal(x - y, expected)

