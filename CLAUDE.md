# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands

- **Install dependencies**: `pixi install` or `pip install -e ".[dev]"`
- **Run tests**: `pixi run test` or `pytest tests/`
- **Run a single test**: `pytest tests/test_main.py::TestMain::test_load_config -v`
- **Lint code**: `pixi run lint` or `ruff check . && mypy .`
- **Format code**: `pixi run format` or `ruff format .`
- **Build package**: `pixi run build` or `python -m build`
- **Run development environment**: `pixi run run-dev`
- **Server tasks**: `pixi run run-frontend` (port 5173), `pixi run run-backend` (port 8081)
- **Restart server**: `pixi run restart-server` (clears cache and restarts)

## Code Style Guidelines

- **Python version**: Must be compatible with Python 3.12+
- **Imports**: Sort imports with `ruff`, use absolute imports
- **Formatting**: Line length 100 characters (per ruff config), follow PEP 8 standards
- **Type hints**: All functions must have complete type annotations (required by mypy)
- **Error handling**: Use specific exception types from `nova_act.types.errors`, wrap exceptions with context
- **Documentation**: Use docstrings with NumPy style (Parameters, Returns, Raises sections)
- **Naming**: Use snake_case for variables/functions, PascalCase for classes
- **Testing**: Write unit tests for all new functionality
- **Packages**: Use relative imports within packages to avoid circular imports