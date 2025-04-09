# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands

- **Install dependencies**: `pixi install` or `pip install -e ".[dev]"`
- **Run tests**: `pixi run test` or `pytest tests/`
- **Run a single test**: `pytest tests/test_main.py::TestMain::test_load_config -v`
- **Lint code**: `pixi run lint` or `ruff check . && mypy .`
- **Format code**: `pixi run format` or `ruff format .`
- **Build package**: `pixi run build` or `python -m build`
- **Run development environment**: `pixi run run-dev` (config: configs/dev.json)
- **Server tasks**: `pixi run run-frontend` (port 5173), `pixi run run-backend` (port 8081)
- **Restart server**: `pixi run restart-server` (clears cache and restarts)
- **Diagnostics**: `pixi run diagnose` (checks system) or `pixi run fix-diagnostics` (auto-fix)

## Example Run Commands

- **Basic example**: `pixi run example-basic` or `python example_nova_act.py` (Simple Google search example)
- **Coffee maker demo**: `pixi run example-coffee` or `pixi run example-coffee-record` (with video recording)
- **Apartment search**: `pixi run example-apartments` or `python -m nova_act.samples.apartments_caltrain [--caltrain_city "Redwood City"] [--bedrooms 2] [--headless]`
- **Setup Chrome profile**: `pixi run example-setup-chrome` (creates a Chrome profile at ./chrome_profile)
- **Order salad example**: `pixi run example-order-salad` (requires Chrome profile setup first)

## Code Style Guidelines

- **Python version**: Must be compatible with Python 3.12+
- **Imports**: Sort imports with `ruff`, use absolute imports between packages
- **Formatting**: Line length 100 characters, follow PEP 8 standards (enforced by ruff)
- **Type hints**: All functions must have complete type annotations (mypy enforces strict typing)
- **Error handling**: Use specific exception types from `nova_act.types.errors`, wrap with context
- **Documentation**: Use NumPy-style docstrings (Parameters, Returns, Raises sections)
- **Naming**: Use snake_case for variables/functions, PascalCase for classes
- **Testing**: Write unit tests for all new functionality
- **Package structure**: Use relative imports within packages to avoid circular imports
- **Project structure**: Frontend (port 5173) and backend (port 8081) run as separate services