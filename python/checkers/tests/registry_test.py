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

"""Tests for checkers.registry."""

import checkers
from checkers import asserts
from checkers import registry
from checkers.runners import pyunit


@checkers.test
def test_registry_init():
  reg = registry.Registry()
  asserts.is_empty(reg)
  asserts.is_empty(reg.keys())
  asserts.is_empty(reg.values())


@checkers.test
def test_registry_register_with_len():
  reg = registry.Registry()
  reg.register('foo', 2)
  reg.register('bar', 4)
  reg.register('baz.quux', 8)
  asserts.are_equal(len(reg), 3)


@checkers.test
def test_registry_attributes():
  reg = registry.Registry()
  reg.register('foo', 2)
  reg.register('bar', 4)
  reg.register('baz.quux', 8)
  asserts.are_equal(reg.foo, 2)
  asserts.are_equal(reg.bar, 4)
  asserts.are_equal(reg.baz__DOT__quux, 8)


@checkers.test
def test_registry_indexers():
  reg = registry.Registry()
  reg.register('foo', 2)
  reg.register('bar', 4)
  reg.register('baz.quux', 8)
  asserts.are_equal(reg['foo'], 2)
  asserts.are_equal(reg['bar'], 4)
  asserts.are_equal(reg['baz.quux'], 8)


@checkers.test
def test_registry_keys():
  reg = registry.Registry()
  reg.register('foo', 2)
  reg.register('bar', 4)
  reg.register('baz.quux', 8)
  asserts.are_equal(reg.keys(), ['foo', 'bar', 'baz.quux'])


@checkers.test
def test_registry_values():
  reg = registry.Registry()
  reg.register('foo', 2)
  reg.register('bar', 4)
  reg.register('baz.quux', 8)
  asserts.are_equal(reg.values(), [2, 4, 8])


@checkers.test
def test_registry_unregister_with_present_key():
  reg = registry.Registry()
  reg.register('foo', 4)
  asserts.are_equal(len(reg), 1)
  reg.unregister('foo')
  asserts.is_empty(reg)


@checkers.test
def test_registry_unregister_with_nonexistent_key():
  reg = registry.Registry()
  reg.unregister('foo')
  asserts.is_empty(reg)


@checkers.test
def test_registry_from_dict():
  values = {'foo': 0, 'bar': 2, 'baz': 'hello', 'quux': False}
  reg = registry.Registry.from_dict(values)
  asserts.has_length(reg, 4)


if __name__ == '__main__':
  pyunit.main()

