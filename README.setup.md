# Setup Instructions

To properly set up the nova-act package for development:

1. First, rename the existing `nova_act` directory at the root level to avoid path conflicts:
```bash
mv nova_act nova_act.old
```

2. Install the package in development mode:
```bash
pip install -e .
```

This will ensure that Python can find the package from the correct location (src/nova_act) while allowing you to modify the code during development.

The package uses a src-layout as specified in pyproject.toml:
```toml
[tool.hatch.build]
packages = ["src"]
```

After following these steps, imports like `from nova_act.nova_act import NovaAct` will work correctly by finding the package in the src/ directory.