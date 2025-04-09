# Nova ACT Package Structure and Installation

## Issue: ModuleNotFoundError: No module named 'nova_act.samples'

This error occurs when Python cannot find the `nova_act.samples` module in its path. The package uses a src-layout structure, which requires specific installation steps to work correctly.

### Package Structure
```
nova-act/
├── src/
│   └── nova_act/
│       └── samples/
│           ├── __init__.py
│           └── order_a_coffee_maker.py
├── setup.py
└── pyproject.toml
```

### Solution

1. Make sure you're in the nova-act directory
2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Technical Details

The package uses a src-layout structure where all source code is under the `src/` directory. This is configured in:

1. setup.py:
   ```python
   setup(
       package_dir={"": "src"},
       packages=find_packages(where="src", include=["nova_act*"])
   )
   ```

2. pyproject.toml:
   ```toml
   [tool.hatch.build]
   packages = ["src"]
   ```

This structure helps prevent import issues during development and ensures proper packaging for distribution.