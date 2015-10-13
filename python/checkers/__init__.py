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

"""Checkers package provides the Checkers framework.

This __init__ module provides the public API for Checkers.
"""

import os
from os import path
import sys
import traceback

import context
import modules
import parameterization
import registry
import test as test_module
import test_case
import test_result
import test_run
import test_suite

# Default extensions/modules
from checkers import asserts as asserts_module
asserts = asserts_module

# pylint: disable=invalid-name

Context = context.Context
Registry = registry.Registry
AutoKeyRegistry = registry.AutoKeyRegistry
Parameterization = parameterization.Parameterization
Test = test_module.Test
FunctionTest = test_module.FunctionTest
TestCase = test_case.TestCase
TestResult = test_result.TestResult
TestResultStatus = test_result.TestResultStatus
TestRun = test_run.TestRun
TestSuite = test_suite.TestSuite

# pylint: enable=invalid-name

################################################################################
# Decorators
################################################################################


def test(function):
  """Decorator that converts a function into a Checkers Test instance.

  Args:
    function: (func) The test case function.

  Returns:
    Test: The Checkers test that wraps the function.
  """
  return FunctionTest(function)


def test_suites(*suite_names):
  """Decorator that adds the test to the set of suites.

  Note that the decorator takes in Test instances, so this decorator should be
  used *above* the @checkers.test decorator (so that the @checkers.test
  decorator will have already been applied and returned a Test instance.)

  Args:
    *suite_names: (strings) Names of suites the test should be added to.

  Returns:
    function: Decorator that will apply suites to the test.
  """

  def test_suites_decorator(checkers_test):
    for suite_name in suite_names:
      checkers_test.test_suite_names.add(suite_name)
    return checkers_test
  return test_suites_decorator


def setup(*setup_functions):
  """Decorator that reigsters setup functions with a test.

  The functions passed in as setup functions take an optional 'context'
  parameter of type checkers.Context.

  Note that the decorator takes in Test instances, so this decorator should be
  used *above* the @checkers.test decorator (so that the @checkers.test
  decorator will have already been applied and returned a Test instance.)

  Args:
    *setup_functions: (functions) Functions to be called before the test runs.

  Returns:
    function: Decorator that will add setup functions to the test.
  """
  def setup_decorator(checkers_test):
    for setup_function in setup_functions:
      checkers_test.setup.register(setup_function)
    return checkers_test
  return setup_decorator


def teardown(*teardown_functions):
  """Decorator that reigsters teardown functions with a test.

  The functions passed in as teardown functions take an optional 'context'
  parameter of type checkers.Context.

  Note that the decorator takes in Test instances, so this decorator should be
  used *above* the @checkers.test decorator (so that the @checkers.test
  decorator will have already been applied and returned a Test instance.)

  Args:
    *teardown_functions: (functions) Functions to be called after the test runs.

  Returns:
    function: Decorator that will add teardown functions to the test.
  """
  def teardown_decorator(checkers_test):
    for teardown_function in teardown_functions:
      checkers_test.teardown.register(teardown_function)
    return checkers_test
  return teardown_decorator


def parameterize(parameterizations):
  """Decorator that adds parameterizations to the test.

  The format of the parameterizations argument is a dict. The key for the dict
  is the name of the parameterization (it will be appended to the test name
  separated by an underscore, so make sure it only includes valid Python
  identifier characters). The value will be basically a variable registry (or
  even just a variable dict) that contains the names and values of each of the
  parameters.

  Note that the decorator takes in Test instances, so this decorator should be
  used *above* the @checkers.test decorator (so that the @checkers.test
  decorator will have already been applied and returned a Test instance.)

  Example:

  import checkers
  from checkers import asserts

  # Will generate test cases test_add_1_1_2, test_add_2_2_4, test_add_0_8_8) :
  @checkers.parameterize({
      '1_1_2': {'x': 1, 'y': 1, 'total': 2},
      '2_2_4': {'x': 2, 'y': 1, 'total': 4},
      '0_8_8': {'x': 0, 'y': 8, 'total': 8},
  })
  @checkers.test
  def test_add(x, y, total):
    asserts.are_equal(x + y, total)

  Args:
    parameterizations: (dict) Named parameterizations to apply to the test.

  Returns:
    function: Decorator that will apply parameterizations to the test.
  """
  def parameterize_decorator(checkers_test):
    for name, params in parameterizations.iteritems():
      p = parameterization.Parameterization(name, params)
      checkers_test.decorator_parameterizations.register(p)
    return checkers_test
  return parameterize_decorator

