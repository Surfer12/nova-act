# Package Import Issue Solution

The issue was caused by having two parallel package structures:
- /nova_act/ (at root level)
- /src/nova_act/ (the correct location)

According to pyproject.toml, this package uses a src-layout:
```toml
[tool.hatch.build]
packages = ["src"]
```

To fix this:
1. Remove the duplicate package structure at root level (done)
2. Ensure you install the package in development mode:
```bash
pip install -e .
```

The package should now correctly import NovaActBridge from the src/nova_act/bridge location.