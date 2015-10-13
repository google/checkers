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

"""Utility functions for working with modules in Checkers."""

from os import path
import sys

import registry
import test


def find_module_name(module, fully_qualified=True):
  """Function that will find the name (sort or fully-qualified) for the module.

  Args:
    module: (module) The module you want the name of.
    fully_qualified: (bool) Whether to give the full name or just the last part.

  Returns:
    string: The name of the module.
  """
  name = module.__name__
  if name != '__main__':
    if not fully_qualified:
      parts = name.split('.')
      return parts[len(parts) - 1]
  elif hasattr(module, '__file__'):
    return path.splitext(path.basename(module.__file__))[0]
  return name

def find_module_name_from_name(module_name, fully_qualified=True):
  """Function that will find the name (sort or fully-qualified) for the module.

  This is useful if the module's name is '__main__' and you want to get the
  file basename.

  Args:
    module_name: (string) The name of the module you want the name of.
    fully_qualified: (bool) Whether to give the full name or just the last part.

  Returns:
    string: The name of the module.
  """
  module = sys.modules[module_name]
  return find_module_name(module, fully_qualified)


def tests_from_module(module, include_imports=False):
  """Finds all of the tests defined in a module and puts them into a registry.

  Args:
    module: (module) The module that we want to look for tests in.
    include_imports: (bool) Whether to search for Tests in the impors, too.

  Returns:
    TestRegistry: The set of discovered tests.

  Raises:
    NotImplementedError: Feature doesn't exist to find tests from imports, yet.
  """
  if include_imports:
    raise NotImplementedError('Searching for tests in imports not supported.')
  test_registry = registry.AutoKeyRegistry(lambda test: test.full_name)
  for attr_name in dir(module):
    attr = getattr(module, attr_name)
    if type(attr) is test.Test:
      # TODO(barkimedes): support tests that are definitions of test classes
      # rather than just instances.
      raise NotImplementedError('Cannot load Test class definitions')
    if isinstance(attr, test.Test):
      test_registry.register(attr)
  return test_registry

