# Getting Started

This guide will help you get started with Nova ACT.

## Prerequisites

Before you begin, make sure you have:

- Python 3.12 or later installed
- A package manager (pip or pixi)
- An Amazon Nova Act API key

## Installation

### Using pip

```bash
pip install nova-act
```

### Using pixi

```bash
pixi add nova-act
```

## Basic Usage

Here's a simple example of how to use Nova ACT:

```python
from nova_act import NovaAct

# Initialize the client
nova = NovaAct(
    nova_act_api_key="your-api-key",
    headless=False  # Set to True for production
)

# Start the client
nova.start()

try:
    # Use the client
    result = nova.act("your command here")
    print(f"Result: {result}")
finally:
    # Always stop the client when done
    nova.stop()
```

## Configuration

Nova ACT can be configured using either:

1. Environment variables
2. Configuration files
3. Direct parameters in the constructor

See the [API Reference](api-reference.md) for more details on configuration options. 