# Contributing to Nova ACT

## Development Setup

1. First, clone the repository:
```bash
git clone https://github.com/yourusername/nova-act.git
cd nova-act
```

2. Rename the existing nova_act directory at root level (if it exists) to avoid import conflicts:
```bash
mv nova_act nova_act.old
```

3. Install the package in development mode:
```bash
pip install -e .
```

This will install the package using the src/ layout, making imports work correctly.

## Running Tests

```bash
pytest
```

The tests expect the package to be installed in development mode as described above.

## Project Structure

The project uses a src layout:
- src/nova_act/: Main package code
  - bridge/: Bridge implementation
  - types/: Type definitions
  - util/: Utility functions