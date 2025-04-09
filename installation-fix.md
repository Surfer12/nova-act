To resolve the ModuleNotFoundError, please ensure you install the package in development mode:

```bash
cd nova-act
pip install -e .
```

The package configuration has been updated to properly include the nova_act.samples module. After installing in development mode, try running the example again:

```bash
pixi run example-setup-chrome
```