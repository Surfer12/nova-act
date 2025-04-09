# Getting Started with Nova ACT

This guide will help you get started with Nova ACT, from installation to your first automation script. Nova ACT provides both Python and Java SDKs, but this guide focuses on the Python implementation.

## Prerequisites

Before you begin, ensure you have:

- Python 3.12 or later installed
- A package manager (pip or pixi)
- An Amazon Nova Act API key
- Chrome or Chromium browser installed

## Installation

The Nova ACT Python SDK is the primary interface documented here. The SDK is located in the `src/nova_act/` directory in the source code.

### Using pip

```bash
# Install the latest version
pip install nova-act

# Install a specific version
pip install nova-act==1.0.0
```

### Using pixi

```bash
# Add to your project
pixi add nova-act

# Add a specific version
pixi add nova-act@1.0.0
```

### Installing from source

If you want to install from source:

```bash
# Clone the repository
git clone https://github.com/amazon/nova-act.git

# Navigate to the directory
cd nova-act

# Install the package
pip install -e .
```

## Project Components

Nova ACT provides multiple implementation options to suit different needs. This guide focuses on the Python SDK, which is the primary and recommended implementation for most users. For a complete overview of all components and their organization, please refer to the [Project Structure](project-structure.md) documentation.

## Basic Usage

Here's a simple example demonstrating the recommended way to use Nova ACT:

```python
from nova_act import NovaAct

# Initialize the client with context manager (recommended)
with NovaAct(
    nova_act_api_key="your-api-key",  # Required
    headless=False,                    # Set to True for production
    screen_width=1920,                 # Customize screen size
    screen_height=1080
) as nova:
    # Perform actions
    result = nova.act("search for python programming")
    print(f"Result: {result}")
```

## Configuration

Nova ACT can be configured through multiple methods:

### 1. Environment Variables

```bash
export NOVA_ACT_API_KEY="your-api-key"
export NOVA_ACT_HEADLESS="true"
export NOVA_ACT_CHROME_CHANNEL="chrome"
```

### 2. Configuration File

Create a `nova_act_config.json` file:

```json
{
    "api_key": "your-api-key",
    "headless": false,
    "chrome_channel": "chrome",
    "screen_width": 1920,
    "screen_height": 1080
}
```

### 3. Constructor Parameters

All configuration options can be passed directly to the `NovaAct` constructor:

```python
nova = NovaAct(
    nova_act_api_key="your-api-key",
    headless=False,
    screen_width=1920,
    screen_height=1080,
    user_data_dir="/path/to/user/data",
    profile_directory="Profile 1"
)
```

## Best Practices

1. **Always use context manager**: The `with` statement ensures proper resource cleanup
2. **Handle errors appropriately**: Use try-except blocks for error handling
3. **Configure logging**: Set up logging for better debugging
4. **Use appropriate timeouts**: Set reasonable timeouts for actions
5. **Clean up resources**: Ensure proper cleanup in case of errors

## Next Steps

- Explore the [API Reference](api-reference.md) for detailed documentation
- Check out [Examples](examples.md) for practical use cases
- Learn about [Error Handling](../CONTRIBUTING.md#error-handling) in the Contributing Guide 