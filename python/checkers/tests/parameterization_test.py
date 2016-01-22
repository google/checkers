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

"""Tests for checkers.parameterization."""

import checkers
from checkers import asserts
from checkers import parameterization
from checkers.runners import pyunit


@checkers.test
def test_parameterization_init():
  param = parameterization.Parameterization('name')
  asserts.are_equal(param.name, 'name')
  asserts.is_empty(param.variables)


@checkers.test
def test_parameterization_with_variables():
  variables = {'foo': 0, 'bar': 2, 'baz': 4, 'quux': 8}
  param = parameterization.Parameterization('name', variables)
  asserts.are_equal(param.name, 'name')
  asserts.has_length(param.variables, 4)


if __name__ == '__main__':
  pyunit.main()
