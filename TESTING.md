# Testing NovaAct

This document describes how to run tests and generate code coverage reports for the NovaAct package.

## Prerequisites

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

## Running Tests

### Using the Test Script

The easiest way to run tests is using the provided script:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

This will:
1. Install the package in development mode
2. Install test dependencies
3. Run all tests with coverage reporting

### Manual Test Execution

Alternatively, you can run tests manually:
```bash
pytest -v --cov=nova_act --cov-report=html --cov-report=term-missing --cov-report=xml tests/
```

## Coverage Reports

After running tests, three types of coverage reports are generated:

1. Terminal Report: Displayed directly in your terminal
2. HTML Report: Located at `htmlcov/index.html`
3. XML Report: Located at `coverage.xml`

### Viewing Coverage Reports

- Terminal: Shows missing lines directly in the console
- HTML: Open `htmlcov/index.html` in your browser for an interactive report
- XML: Used for CI/CD integration and tools like SonarQube

## Test Structure

Tests are organized into several files:
- `test_nova_act_core.py`: Core functionality tests
- `test_nova_act_browser.py`: Browser interaction tests
- `test_nova_act_utils.py`: Utility function tests

## Configuration

Test configuration is split across several files:
- `pyproject.toml`: Main pytest configuration
- `.coveragerc`: Coverage.py configuration
- `conftest.py`: Pytest fixtures and shared resources

## Writing New Tests

1. Create a new test file in the `tests/` directory
2. Use the `@pytest.mark.asyncio` decorator for async tests
3. Use fixtures from `conftest.py` where appropriate
4. Run tests to ensure coverage is maintained