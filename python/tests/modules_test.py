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

"""Tests for checkers.modules_test."""

import sys

import checkers
from checkers import asserts
from checkers import modules
from checkers.runners import pyunit


@checkers.test_suites('find_module_name')
@checkers.test
def test_find_module_name():
  module = sys.modules[__name__]
  name = modules.find_module_name(module)
  asserts.are_equal('modules_test', name)


@checkers.test_suites('find_module_name')
@checkers.test
def test_find_module_name_short():
  name = modules.find_module_name(asserts, fully_qualified=False)
  asserts.are_equal('asserts', name)


@checkers.test_suites('find_module_name_from_name')
@checkers.test
def test_find_module_name_from_name():
  name = modules.find_module_name_from_name(__name__)
  asserts.are_equal('modules_test', name)


@checkers.test
def test_tests_from_module():
  module = sys.modules[__name__]
  tests = modules.tests_from_module(module)
  asserts.are_equal(len(tests), 4)


if __name__ == '__main__':
  pyunit.main()
