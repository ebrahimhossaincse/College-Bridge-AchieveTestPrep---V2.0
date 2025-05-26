import pytest

# List of test files or directories to run
test_files = [
    "tests/test_college_bridge.py"
]

# Add Allure reporting arguments
allure_args = [
    "--alluredir=reports/allure-results",
    "--clean-alluredir"  # Optional: Cleans the directory first
]

# Combine test files and allure arguments
pytest_args = test_files + allure_args

exit_code = pytest.main(pytest_args)