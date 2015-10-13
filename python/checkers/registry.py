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

"""Defines Registry classes that can hold named key/value collections."""

import collections

_IDENTIFIER_REPLACEMENTS = {
    '.': '__DOT__',
}


def to_identifier(raw_string):
  """Given a string, converts it into a valid Python identifier.

  This function is mainly targeted at fixing fully-qualified type names so that
  they can be used as IDs. For example, any '.'s will be converted to __DOT__.

  The important thing to note here is that anything that is already a valid
  identifier will not be affected.

  Args:
    raw_string: (string) The string to convert into an identifier.

  Returns:
    string: The (hopefully) valid Python identifier with translated characters.
  """
  result = raw_string
  for original, replacement in _IDENTIFIER_REPLACEMENTS.iteritems():
    result = result.replace(original, replacement)
  return result


class Registry(collections.MutableMapping):
  """A Registry is basically a dictionary where keys also become attributes."""

  def __init__(self):
    """Initializes a new instance of a registry."""
    self._values = collections.OrderedDict()

  @staticmethod
  def from_dict(source):
    """Creates a registry from the provided dictionary.

    Args:
      source: (dict) Source whose items should be copied into the registry.

    Returns:
      Registry: A new registry populated with the source elements.
    """
    registry = Registry()
    for k, v in source.iteritems():
      registry.register(k, v)
    return registry

  def __len__(self):
    """Gets the number of values in the registry."""
    return len(self._values)

  def __getitem__(self, key):
    """Gets the item with the given key from the registry."""
    return self._values[key]

  def __setitem__(self, key, value):
    """Sets the provided value to the given key in the registry."""
    self._values[key] = value
    setattr(self, to_identifier(key), value)

  def __delitem__(self, key):
    """Deletes the item with the given key from the registry."""
    if key in self._values:
      self._values.pop(key, None)
      delattr(self, to_identifier(key))

  def __iter__(self):
    """Gets an iterator to the registry."""
    return iter(self._values)

  def register(self, key, value):
    """Adds (or replaces) an item with the given key in the registry.

    Args:
      key: (string) The (unique) name of the item being registered.
      value: (anything) The actual item being registered.
    """
    self[key] = value

  def unregister(self, key):
    """Removes the item with the key from the registry.

    Args:
      key: (string) The name of the item being unregistered.
    """
    del self[key]

  def merge(self, source, replace_existing=False):
    """Merge the contents of the given registry with this registry.

    Args:
      source: (dict) The dictionary containing items to copy into this registry.
      replace_existing: (bool) Whether to overwrite existing entries.
    """
    for key, value in source.iteritems():
      if key in self and not replace_existing:
        continue
      self.register(key, value)


class AutoKeyRegistry(Registry):
  """Registry that uses a function to automatically figure out the key.

  This is useful for registries where the key can be gleaned from the object
  being registered.
  """

  def __init__(self, autokey_function):
    """Initializes a new AutoKeyRegistry using the given autokey function.

    The autokey function should be used to take in an item and return the key
    that should be used for that item. For example, a test_case can be keyed on
    the test case's full_name attribute, so we could define such a registry
    like this:

    test_case_registry = AutoKeyRegistry(lambda tc: tc.full_name)

    Args:
      autokey_function: (function) Takes in an item and returns the key for it.
    """
    super(AutoKeyRegistry, self).__init__()
    self.autokey_function = autokey_function

  def register(self, value):
    """Adds (or replaces) an item with the given key in the registry.

    Args:
      value: The [autokeyed] item being added to the registry.
    """
    super(AutoKeyRegistry, self).register(self.autokey_function(value), value)

  def merge(self, source, replace_existing=False):
    """Merge the contents of the given registry with this registry.

    Args:
      source: (dict) The dictionary containing items to copy into this registry.
      replace_existing: (bool) Whether to overwrite existing entries.
    """
    for key, value in source.iteritems():
      if key in self and not replace_existing:
        continue
      self.register(value)


class SuperRegistry(Registry):
  """Registry in which the value is another registry.

  This is useful in situations where you want to register an item, but it needs
  to be grouped. For example, parameterizations need to be grouped by the test
  that they're parameterizing, so the key would be the full test name and the
  value would be a parameterization registry.
  """

  def __init__(self, subregistry_factory):
    super(SuperRegistry, self).__init__()
    self.subregistry_factory = subregistry_factory

  def register(self, key, value):
    if key not in self.keys():
      super(SuperRegistry, self).register(key, self.subregistry_factory())
    self[key].register(value)

