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

python setup.py install --user

echo 'python/tests/checkers_test.py'
python python/tests/checkers_test.py

echo 'python/tests/context_test.py'
python python/tests/context_test.py

echo 'python/tests/modules_test.py'
python python/tests/modules_test.py

echo 'python/tests/parameterization_test.py'
python python/tests/parameterization_test.py

echo 'python/tests/registry_test.py'
python python/tests/registry_test.py

echo 'python/tests/test_case_test.py'
python python/tests/test_case_test.py

echo 'python/tests/test_result_test.py'
python python/tests/test_result_test.py

echo 'python/tests/test_run_test.py'
python python/tests/test_run_test.py

echo 'python/tests/test_suite_test.py'
python python/tests/test_suite_test.py

echo 'python/tests/test_test.py'
python python/tests/test_test.py

echo 'python/tests/asserts/asserts_test.py'
python python/tests/asserts/asserts_test.py

