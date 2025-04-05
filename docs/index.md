# Nova ACT

Welcome to the Nova ACT documentation! This Python SDK provides a powerful interface for interacting with Amazon Nova Act.

## Features

- Easy-to-use Python interface
- Comprehensive API coverage
- Robust error handling
- Extensive documentation
- Type hints for better IDE support

## Quick Start

```python
from nova_act import NovaAct

# Initialize the client
nova = NovaAct()

# Start the client
nova.start()

# Use the client
result = nova.act("your command here")

# Stop the client
nova.stop()
```

## Installation

You can install Nova ACT using pip:

```bash
pip install nova-act
```

Or using pixi:

```bash
pixi add nova-act
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details. 