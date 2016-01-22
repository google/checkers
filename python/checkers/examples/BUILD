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
#   Examples showing how to use different features of Checkers.

test_suite(
    name = "small_tests",
    tags = ["small"],
    visibility = ["//:__pkg__"],
)

py_test(
    name = "hello_world_test",
    size = "small",
    srcs = [
        "hello_world_test.py",
    ],
    visibility = ["//:__pkg__"],
    deps = [
        "//checkers",
        "//checkers/runners/pyunit",
    ],
)

py_test(
    name = "explicit_hello_world_test",
    size = "small",
    srcs = [
        "explicit_hello_world_test.py",
    ],
    visibility = ["//:__pkg__"],
    deps = [
        "//checkers",
        "//checkers/runners/pyunit",
    ],
)

py_test(
    name = "suite_example_test",
    size = "small",
    srcs = [
        "subtraction_tests.py",
        "suite_example_test.py",
    ],
    visibility = ["//:__pkg__"],
    deps = [
        "//checkers",
        "//checkers/runners/pyunit",
    ],
)

py_test(
    name = "fixtures_test",
    size = "small",
    srcs = [
        "calculator.py",
        "fixtures_test.py",
    ],
    visibility = ["//:__pkg__"],
    deps = [
        "//checkers",
        "//checkers/runners/pyunit",
    ],
)

py_test(
    name = "parameterization_example_test",
    size = "small",
    srcs = [
        "calculator.py",
        "parameterization_example_test.py",
    ],
    visibility = ["//:__pkg__"],
    deps = [
        "//checkers",
        "//checkers/runners/pyunit",
    ],
)

