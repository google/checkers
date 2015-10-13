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

"""Checkers setup.py script."""

from distutils.core import setup

setup(
    name='pycheckers',
    version='0.1',
    description='Functional, dependency-injected test framework for Python.',
    maintainer='Google',
    author='Sabrina Williams',
    # maintainer_email='checkers google group or something',
    # url='github url',
    package_dir={
        'checkers.examples': 'examples',
        'checkers.tests': 'tests',
    },
    packages=[
        'checkers',
        'checkers.asserts',
        'checkers.examples',
        'checkers.runners.pyunit',
        'checkers.tests',
    ],
)

