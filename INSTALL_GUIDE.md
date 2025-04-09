# Installation Guide for nova-act

To resolve the `ModuleNotFoundError: No module named 'nova_act.samples'` issue, please follow these installation steps:

1. Ensure you are in the project root directory (nova-act)

2. Activate your pixi environment:
   ```bash
   pixi shell
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

This will install the package with all submodules (including `nova_act.samples`) properly linked in your pixi environment.

## Why this works

The package uses a src-layout structure where the code is in the `src/` directory. We've configured both `setup.py` and `pyproject.toml` to handle this layout, but the package needs to be installed in development mode (-e) to ensure Python can find all the modules correctly.

When installed with `-e`, pip creates links to your source code instead of copying it, which is ideal for development and ensures all submodules are properly recognized.