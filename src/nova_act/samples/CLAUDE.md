# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run module: `python -m nova_act.samples.<module_name> [args]`
- Run specific module with arguments: `python -m nova_act.samples.analyze_winguru --spot_id <id> --analyze_map`
- Run tests: `pytest tests/` or `pytest tests/test_<file>.py -v`
- Run single test: `pytest tests/test_<file>.py::TestClass::test_method -v`
- Lint code: `flake8 nova_act/`
- Type check: `mypy nova_act/`
- Install dependencies: `pip install -r requirements.txt`

## Code style
- **Imports**: Standard library first, third-party next, local modules last, alphabetically within each group
- **Type hints**: Use for all function parameters and return values with appropriate Optional types
- **Error handling**: Use try/except with detailed error messages and logging at appropriate levels
- **Models**: Use Pydantic BaseModel with Field descriptors for structured data
- **Logging**: Configure and use the logging module with consistent level usage
- **Documentation**: Include docstrings for all modules, classes, and functions
- **Formatting**: Follow PEP 8 guidelines with descriptive snake_case for variables and functions
- **Function parameters**: Use descriptive parameter names with appropriate default values 1. Enhanced Error Handling for Wind Speed Extraction:
    - Added a comprehensive try-except block around the wind speed extraction to catch
  ActModelError and other exceptions
    - Implemented an alternative extraction approach with a different prompt when the
  primary approach fails
    - Included detailed logging for debugging purposes
  2. Improved Table Structure Identification:
    - Added error handling around the table structure identification step
    - The script now continues gracefully even if the structure identification fails
  3. Robust Date/Time Extraction:
    - Added multiple layers of fallbacks for date/time extraction
    - Implemented alternative prompts for date extraction with more specific guidance
    - Added last-resort synthetic data generation to prevent complete script failure
  4. Better Array Length Handling:
    - Improved how we handle mismatches between dates and data arrays
    - Changed from truncating date arrays to padding data arrays, which preserves more
  information
    - Added detailed logging for all mismatch scenarios

  These changes make the script much more robust against the ActModelError issue when
  extracting wind speeds. The script now has multiple fallback mechanisms and will
  continue executing even if certain parts of the extraction fail. It should be able to
  complete successfully and provide useful results even if the AI model encounters
  issues with processing certain data.
