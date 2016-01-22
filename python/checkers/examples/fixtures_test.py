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

"""Example of how to use various types of test fixtures within Checkers."""

import checkers
from checkers import asserts
from checkers.examples.calculator import Calculator
from checkers.runners import pyunit


def logging_test_run_setup(test_run):
  print '#' * 80
  print 'Starting test run:', test_run.name


def logging_test_run_teardown(test_run):
  print 'Finishing test run:', test_run.name
  print '#' * 80


def register_calculator(context):
  calc = Calculator()
  print 'Registering calculator:', context.test_case.name, calc.__class__
  context.variables.register('calculator', calc)


def logging_test_case_setup(context):
  print '*' * 80
  print 'Starting test case:', context.test_case.full_name


def logging_test_case_teardown(context):
  print 'Finishing test case:', context.test_case.full_name
  print '*' * 80


def celebrate_evenness(context):
  print 'Awesome!! %s only has even numbers!!' % context.test_case.name


def curse_oddness(context):
  print 'Phooey!! %s has odd numbers :P' % context.test_case.name


def zero_division_setup():
  print 'Oops, dividing by zero in this test'


@checkers.setup(celebrate_evenness, zero_division_setup)
@checkers.test
def test_divide_2_0():
  with asserts.expect_exception(ZeroDivisionError):
    2 / 0

@checkers.teardown(curse_oddness)
@checkers.test
def test_add_1_1_2(calculator):
  asserts.are_equal(calculator.add(2, 2), 4)
  print '1 + 1 = 2'


@checkers.setup(celebrate_evenness)
@checkers.test
def test_add_2_2_4(calculator):
  asserts.are_equal(calculator.add(2, 2), 4)
  print '2 + 2 = 4'


@checkers.setup(celebrate_evenness)
@checkers.test
def test_add_4_8_12(calculator):
  asserts.are_equal(calculator.add(4, 8), 12)
  print '4 + 8 = 12'


def create_test_run():
  test_run = checkers.TestRun.from_module()
  test_run.setup.register(logging_test_run_setup)
  test_run.teardown.register(logging_test_run_teardown)
  test_run.test_case_setup.register(logging_test_case_setup)
  test_run.test_case_setup.register(register_calculator)
  test_run.test_case_teardown.register(logging_test_case_teardown)
  return test_run


if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())

