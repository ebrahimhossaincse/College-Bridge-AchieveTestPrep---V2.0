import pytest

# List of test files or directories to run
test_files = [
    "tests/test_college_bridge2.py"
]

exit_code = pytest.main(test_files)
