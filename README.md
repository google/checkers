# Checkers Test Framework

[![Build Status](https://api.travis-ci.org/google/checkers.png)](https://travis-ci.org/google/checkers)

Checkers is a flexible test authoring framework for Python.

You may find Checkers useful if you want to do any of the following:

* Have more control over how tests are structured.
* Treat the components under test as external dependencies.
* Define tests as standalone functions rather than methods in test classes.
* Run data-driven (parameterized) tests.

Checkers is designed around the idea that tests are really composed of several
parts: test steps, test data, components under test, and test metadata. Checkers
allows the user to have control over all of these areas, so it is easy to
customize behavior. However, default behaviors are implemented so that writing
simple tests is still super simple.


## Requirements

Python 2.7

## Installation

TODO(barkimedes): Describe installation in more detail. This is just a general
recommendation for people who already know how to download code from GitHub.

* Download (or clone) the google/checkers repository.
* From the python folder, run `python setup.py install`
* ...
* ~~Profit!!~~ Test!!

## Quick Start

The following is a very simple Checkers test:

```python
import checkers
from checkers import asserts
from checkers.runners import pyunit

@checkers.test
def test_add_2_2_4():
  asserts.are_equal(2 + 2, 4)

@checkers.test
def test_add_4_8_12():
  asserts.are_equal(4 + 8, 12)

@checkers.test
def test_divide_2_0_error():
  with asserts.expect_exception(ZeroDivisionError):
    2 / 0


if __name__ == '__main__':
  pyunit.main()
```

Remember when we mentioned that tests are composed of several parts? Well, a
couple of them are evidenced here.

First, a test must have some test steps. Consider this the test logic. With
Checkers, this is indicated by functions that are decorated with
`@checkers.test`. Each of these functions becomes a `checkers.Test` instance.

Secondly, we must have a test runner. Checkers tests can be run by anything that
knows how to deal with `checkers.TestRun`(s), but a test runner that is
distributed with Checkers is the PyUnit runner. This is used in the `main`
function here. (By default, the runner will include all of the tests in the
module containing `main`).

### Defining Test Runs

Tests are always placed into test runs (`checkers.TestRun` instances). In the
above example, the test run was created automatically by the `pyunit.main`
function. But if you want to do anything interesting, you'll probably need to
create and manage your test runs directly.

The test run allows you to provide lots of things to the test. You can register
`setup` and `teardown` functions (at the test run level, `setup` will run once
before all of the tests and then `teardown` will run once after all of the tests
are complete). You can also define test suite for organizing test cases. You can
add tests directly to the test run from wherever you like. You can register
components to be injected into the test cases. Here is a more interesting test
case that does a few of those things:

Before we get too fancy, let's see the above example where we explicitly create
the test run:

```python
import checkers
from checkers import asserts
from checkers.runners import pyunit

@checkers.test
def test_add_2_2_4():
  asserts.are_equal(2 + 2, 4)

@checkers.test
def test_add_4_8_12():
  asserts.are_equal(4 + 8, 12)

def create_test_run():
  test_run = checkers.TestRun()
  test_run.tests.register(test_add_2_2_4)
  rest_run.tests.register(test_add_4_8_12)
  # You can also load tests by module so you don't have to register each test.
  # If module_name isn't provided, it defaults to '__main__'
  # test_run = checkers.TestRun.from_module(module_name=__name__)
  return test_run

if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())
```

### Injecting Components

Now that we know how to create a test run, let's see how component injection
works.

Imagine we have a `Calculator` class that is the component-under-test and we
want to inject it into the tests. `Calculator` is defined in the `calculator.py`
module as follows:

```python
class Calculator(object):

  def add(self, x, y):
    return x + y

  def subtract(self, x, y):
    return x - y

  def multiply(self, x, y):
    return x * y

  def divide(self, x, y):
    return x / y
```

Exciting, right? Now let's take our original two tests and update them to use
the calculator to do the adding.

```python
import calculator

import checkers
from checkers import asserts
from checkers.runners import pyunit

@checkers.test
def test_add_2_2_4(calculator):
  asserts.are_equal(calculator.add(2, 2), 4)

@checkers.test
def test_add_4_8_12(calculator):
  asserts.are_equal(calculator.add(4, 8), 12)

def create_test_run():
  test_run = checkers.TestRun.from_module()
  test_run.variables.register('calculator', calculator.Calculator)
  return test_run

if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())
```

Tests can take in arguments. In the above example, the tests take in a
`calculator` argument. These arguments are referred to as 'variables' in
Checkers. So if you want all of the tests in a test run to have access to a
particular variable and value (in this case, a `Calculator` instance), then
just register it with the test run variables and Checkers will inject it for you
when the test runs.

### Data-Driven (Parameterized) Tests

Test variables don't just have to be components under test. There is another
mechanism for passing values into tests: parameterization. And good news!! It's
built natively into Checkers, so it works pretty well :)

There are two ways that you can parameterize a test. One way is through the
`@checkers.parameterize` decorator. The other way is to register the
parameterizations through the test run. Hopefully this isn't too confusing, but
test run-based parameterizations are a useful feature because sometimes a
parmeterization is only  useful in certain circumstances/under certain
configurations, and this allows us to not *always* have a parameterization
applied to test cases (which is the case when decorators alone provide this
functionality).

Anywho, the following example shows both ways of adding parameterizations:

```python
import checkers
from checkers import asserts
from checkers.runners import pyunit

import calculator as calc


@checkers.test
def test_add(calculator, x, y, expected):
  asserts.are_equal(calculator.add(x, y), expected)
  print '%d + %d = %d' % (x, y, expected)


# In this example, the parameterization is applied directly to the test method.
# That means that these parameterizations will always be applied whenever this
# test is used in a test run. Use with caution!
@checkers.parameterize({
    '8_2_6': {'x': 8, 'y': 2, 'expected': 6},
    '0_1_n1': {'x': 0, 'y': 1, 'expected': -1},
})
@checkers.test_suites('subtract')
@checkers.test
def test_subtract(calculator, x, y, expected):
  asserts.are_equal(calculator.subtract(x, y), expected)
  print '%d - %d = %d' % (x, y, expected)


# Since the parameterizations are defined in a function, you can imagine using
# this in a wide variety of scenarios. For example, you could have code here
# that parses test data from a data file or grabs it from a datastore of some
# sort. This provides a built-in, flexible parameterization.
def build_add_params():
  return [
      checkers.Parameterization('1_1_2', {'x': 1, 'y': 1, 'expected': 2}),
      checkers.Parameterization('2_2_4', {'x': 2, 'y': 2, 'expected': 4}),
      checkers.Parameterization('4_8_12', {'x': 4, 'y': 8, 'expected': 12}),
      checkers.Parameterization('2_n1_1', {'x': 2, 'y': -1, 'expected': 1}),
  ]


def create_test_run():
  test_run = checkers.TestRun.from_module()
  test_run.variables.register('calculator', calc.Calculator())
  # The parameterizations are applied at the test run level, so they only apply
  # to this test run.
  # You should prefer this mechanism for creating parameterizations that may be
  # dependent on the environment, that you have to load data from another
  # location (like a database), or where the components under test may behave
  # differently from each other so the parameters would have to change between
  # test runs.
  for param in build_add_params():
    test_run.parameterizations.register(test_add.full_name, param)
  return test_run


if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())
```

The output of running the above test is the following:

```
Running tests under Python 2.7.6: /path/to/python2.7
........
----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
1 + 1 = 2
2 + 2 = 4
4 + 8 = 12
2 + -1 = 1
8 - 2 = 6
0 - 1 = -1
```

Note that components and parameter values are both just variables. So
functionally, it is entirely possible to include a component in a
parameterization (and vice versa). But conceptually, you probably want to make
sure that you're keeping the two straight.


### Test Fixtures

Checkers supports fixtures at the test run and test case levels. If you have
`setup` and/or `teardown` function(s) that you want to run once per test run,
they can be registered with the test run instance. If you have `setup` and/or
`teardown` functions that you want to run before or after each individual test
case, then you can use the `@checkers.setup` and `@checkers.teardown` decorators
on tests themselves, or register them with the test run.

Note that test run-level fixtures will take in an optional parameter: the
`checkers.TestRun` instance. A test case-level fixture will take in an optional
`checkers.Context` instance.

The cool thing about Checkers fixtures is that you can have as many or as few
as you like, and they can be defined as functions with names that actually
make sense and can be shared. (In general, Checkers is very friendly to mixing
and matching things however you like.)

There is a special variable in Checkers that is available to any test function.
The `context` variable will always contain a `checkers.Context` instance, which
contains information about the test run, the test case itself, etc. You'll see
that in this example, too.

```python
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
```

The output for the above test run would be as follows:

```plain
################################################################################
Starting test run: fixtures_test
********************************************************************************
Starting test case: fixtures_test.test_add_1_1_2
Registering calculator: test_add_1_1_2 <class 'calculator.Calculator'>
1 + 1 = 2
Phooey!! test_add_1_1_2 has odd numbers :P
Finishing test case: fixtures_test.test_add_1_1_2
********************************************************************************
********************************************************************************
Starting test case: fixtures_test.test_add_2_2_4
Registering calculator: test_add_2_2_4 <class 'calculator.Calculator'>
Awesome!! test_add_2_2_4 only has even numbers!!
2 + 2 = 4
Finishing test case: fixtures_test.test_add_2_2_4
********************************************************************************
********************************************************************************
Starting test case: fixtures_test.test_add_4_8_12
Registering calculator: test_add_4_8_12 <class 'calculator.Calculator'>
Awesome!! test_add_4_8_12 only has even numbers!!
4 + 8 = 12
Finishing test case: fixtures_test.test_add_4_8_12
********************************************************************************
Finishing test run: fixtures_test
################################################################################
Running tests under Python 2.7.6: /path/to/python2.7
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

## Test Organization

Checkers makes it easy to organize your tests in a flexible, fluid kind of way.

A nice aspect of Checkers is that you can use test suites to organize tests. An
even nicer aspect is that the same test can be part of muliple test suites!!
This can be really cool if you either have multiple ways that you want to view
test results (perhaps one view is by module and another view is by feature). It
can also be helpful if you want the same test to be part of multiple suites
(like if tests are grouped by feature and this is an integration test that
covers multiple features). The nicest feature about using test suites is that,
even if a test is used in multiple suites, it is only run once (assuming the
test runner that you're using is well-implemented, of course).

I take that back. The *nicest* feature is that you can use this mechanism to
distribute your test definitions cleanly in various modules and use suites to
bring them together in test runs in ways that make sense.

You can assign tests to test suites in a few ways. One way is through the
`@checkers.test_suites` decorator. Another way is to create a
`checkers.TestSuite` instance and register the whole suite with the test run.
You can just register a test directly in the test run. Lastly, you can add a
variable to a parameterization called 'test_suites' that has a list of suite
names that only that parameterization should apply to. Let's see all of these
options below.

Imagine we've defined some subtraction tests in a separate module.

```python
import checkers
from checkers import asserts

@checkers.parameterize({
    '8_2_6': {'x': 8, 'y': 2, 'expected': 6},
    '0_1_n1': {'x': 0, 'y': 1, 'expected': -1},
})
@checkers.test
def test_subtract(x, y, expected):
  return asserts.are_equal(x - y, expected)
```

And in our main module, we can see all of the different ways that test suites
can be defined (decorator, part of a parameterization, registered with the test
run, or as individual tests registered with the test run).

```python
import checkers
from checkers import asserts
from checkers.runners import pyunit

import subtraction_tests

@checkers.test_suites('addition', 'multiplication')
@checkers.parameterize({
    '0_0': {'x': 0, 'expected': 0, 'test_suites': ['identity']},
    '1_2': {'x': 1, 'expected': 2},
    '4_8': {'x': 4, 'expected': 8},
    'n2_n4': {'x': -2, 'expected': -4},
})
@checkers.test
def test_double(x, expected):
  asserts.are_equal(x + x, expected)
  asserts.are_equal(x * 2, expected)

@checkers.parameterize({
    '0_1_1': {'x': 0, 'y': 1, 'expected': 1, 'test_suites': ['identity']},
    '1_2_3': {'x': 1, 'y': 2, 'expected': 3},
    '4_8_12': {'x': 4, 'y': 8, 'expected': 12},
})
@checkers.test
def test_add(x, y, expected):
  asserts.are_equal(x + y, expected)


def create_test_run():
  test_run = checkers.TestRun.from_module()
  test_run.test_suites['addition'].register(test_add)
  subtraction_suite = checkers.TestSuite.from_module(subtraction_tests)
  test_run.test_suites.register(subtraction_suite)
  return test_run

if __name__ == '__main__':
  pyunit.main(test_run=create_test_run())
```

If you ran that code, you'd see that 24 tests were run. In reality, only 9 tests
were *actually* executed. But in the report, since they're grouped by suites and
some tests are in multiple suites, it is reported as 24 tests. If nothing else,
you can use Checkers to grossly inflate your metrics and impress folks with your
prolific test authoring!! :smiling_imp:

## Asserts Module (`checkers.asserts`)

You can use any assert engine for doing asserts, from using the `assert`
statement directly to using a full-blown matching framework like
[PyHamcrest](https://pypi.python.org/pypi/PyHamcrest). Checkers comes with a few
built-in asserters in the `checkers.asserts` module.

Assert | Example | Description
-------|---------|------------
`expect_exception` | `with asserts.expect_exception(ZeroDivisionError): 2 / 0` | asserts that the expected exception is raised
`is_true` | `asserts.is_true(True)` | asserts that the the condition passed in evaluates to true
`is_false` | `asserts.is_false(False)` | asserts that the condition passed in evaluates to false
`are_equal` | `asserts.are_equal(2, 2)` | asserts that the two values are equal (using ==)
`are_not_equal` | `asserts.are_not_equal(2, 4)` | asserts that the two values are not equal (using ==)
`is_in` | `asserts.is_in(2, [0, 2, 4, 8])` | asserts that the item is in the collection (using the `in` keyword)
`is_not_in` | `asserts.is_not_in(1, [0, 2, 4, 8])` | asserts that the item is not in the collection (using the `in` keyword)
`is_empty` | `asserts.is_empty('')` | asserts that the collection has a length of 0
`is_not_empty` | `asserts.is_not_empty('hello')` | asserts that the collection has length > 0
`is_none` | `asserts.is_none(None)` | asserts that the provided value evaluates to None (not just falsey)
`is_not_none` | `asserts.is_not_none(0)` | asserts that the provided value evaluates to a non-None value
`are_same` | `asserts.are_same(0, 0)` | asserts that the two values are the same (using `is` keyword)
`are_not_same` | `asserts.are_not_same([0, 2], [0, 2]` | asserts that the two values are not the same (using `is` keyword)
`has_length` | `asserts.has_length('hello', 5)` | asserts that the given iterable has the expected length

## Test Runners (`checkers.runners.pyunit`)

The included test runner in the package is the PyUnit runner. This will run the
Checkers tests *in addition to any other existing unittest-based tests.* The
`pyunit.main` function will call `unittest.main`, and pass through any provided
args, so it is very easy to integrate Checkers into existing test environments.

As mentioned previously, tests are always stored in test runs in Checkers. So
any test runner can be used that takes in test run(s) and executes them.

## Disclaimer
This is not an official Google product (experimental or otherwise), it is just
code that happens to be owned by Google.

