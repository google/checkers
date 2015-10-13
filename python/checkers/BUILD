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

# Description:
#   The Checkers testing framework provides an alternative to writing PyUnit-
#   based tests. Namely, you can define your tests as parameterized functions
#   and Checkers does the work of mapping the test's parameterizations and
#   and dependencies to the parameters in the test. For more information, see
#   the documentation at TODO(barkimedes): link to documentation here.

py_library(
    name = "checkers",
    srcs = [
        "__init__.py",
        "context.py",
        "modules.py",
        "parameterization.py",
        "registry.py",
        "test.py",
        "test_case.py",
        "test_result.py",
        "test_run.py",
        "test_suite.py",
    ],
    visibility = ["//visibility:public"],
    deps = ["//checkers/asserts"],
)

