# Nova ACT

Welcome to the Nova ACT documentation! Nova ACT is a powerful Python SDK that enables seamless interaction with Amazon Nova Act, providing an intuitive interface for web automation and AI-driven actions.

## Key Features

- 🤖 **AI-Powered Automation**: Leverage advanced AI to perform complex web actions
- 🚀 **Easy Integration**: Simple Python interface with comprehensive API coverage
- 🛡️ **Robust Error Handling**: Built-in error management and recovery mechanisms
- 📚 **Extensive Documentation**: Detailed guides and examples for all use cases
- 💡 **Type Hints**: Full type support for better IDE integration and code completion
- 🔄 **Context Management**: Support for Python's context manager protocol
- 🎯 **Schema Validation**: Built-in support for response validation using JSON schemas

## Project Structure

Nova ACT is a multi-component project organized as follows:

- **Python SDK**: Located in `src/nova_act/`, this is the primary Python implementation documented here.
- **Java SDK**: Located in `main/java/com/amazon/novaact/`, provides Java bindings for Nova ACT.
- **Web Frontend**: Located in `src/frontend/`, contains the React TypeScript web application.

For most users, the Python SDK in `src/nova_act/` is the recommended interface.

## Quick Start

```python
from nova_act import NovaAct

# Initialize and use the client with context manager
with NovaAct() as nova:
    # Perform actions
    result = nova.act("search for python programming")
    print(f"Result: {result}")
```

## Installation

Choose your preferred installation method:

```bash
# Using pip
pip install nova-act

# Using pixi
pixi add nova-act
```

## Documentation

- [Getting Started](getting-started.md) - Set up and basic usage
- [API Reference](api-reference.md) - Detailed API documentation
- [Examples](examples.md) - Practical usage examples
- [Project Structure](project-structure.md) - Project organization and recommendations

## Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details on how to get involved.

## Support

For support, please:
- Check the [documentation](getting-started.md)
- Review [common issues](../CONTRIBUTING.md#common-issues)
- Open an issue on our GitHub repository 