# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run module: `python -m nova_act.samples.<module_name> [args]`
- Run tests: `pytest tests/` or `pytest tests/test_<file>.py -v`
- Lint code: `flake8 nova_act/`
- Type check: `mypy nova_act/`

## Code style
- Imports: Standard library first, third-party next, local modules last
- Type hints: Use for all function parameters and return values  
- Error handling: Use try/except with detailed error messages and logging
- Models: Use Pydantic models for structured data
- Logging: Use the logging module with appropriate levels
- Documentation: Docstrings for modules, classes, and functions
- Formatting: Follow PEP 8 guidelines 
- Variable names: Use descriptive snake_case for variables and functions