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

"""Tests for checkers.context."""

import checkers
from checkers import asserts
from checkers import context
from checkers.runners import pyunit


class _DummyTestCase(object):
  """Dummy test case class since we don't use it for anything useful."""
  pass


class _DummyTestRun(object):
  """Dummy test run class since we don't use it for anything useful."""
  pass


@checkers.test
def test_context_init():
  tc = _DummyTestCase()
  tr = _DummyTestRun()
  ctx = context.Context(tc, tr)
  asserts.are_same(tc, ctx.test_case)
  asserts.are_same(tr, ctx.test_run)
  asserts.are_equal(len(ctx.variables), 1)
  asserts.is_in('context', ctx.variables)


@checkers.test
def test_context_init_with_args():
  tc = _DummyTestCase()
  tr = _DummyTestRun()
  ctx = context.Context(tc, tr, foo='foo', bar=2)
  asserts.are_same(tc, ctx.test_case)
  asserts.are_same(tr, ctx.test_run)
  asserts.are_equal(len(ctx.variables), 3)
  asserts.are_equal(ctx.variables.foo, 'foo')
  asserts.are_equal(ctx.variables.bar, 2)
  asserts.is_in('context', ctx.variables)


if __name__ == '__main__':
  pyunit.main()

