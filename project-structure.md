# Project Structure

Nova ACT is organized into several key components, each serving a specific purpose in the ecosystem:

## Core Components

### Python SDK (`src/nova_act/`)
The primary and recommended implementation for most users. The Python SDK provides:
- Core automation functionality
- Full type hints support
- Comprehensive error handling
- Built-in schema validation
- Context manager support

### Java SDK (`main/java/com/amazon/novaact/`)
Java language bindings for Nova ACT, offering:
- Native Java interface to Nova ACT functionality
- Integration with Java ecosystem
- Enterprise-ready implementation
- Thread-safe operations

### Web Frontend (`src/frontend/`)
React TypeScript web application that provides:
- Visual interface for Nova ACT operations
- Real-time monitoring and control
- Configuration management
- Results visualization

## Supporting Components

### Documentation (`docs/`)
Comprehensive documentation including:
- Getting Started guide
- API Reference
- Usage Examples
- Best Practices
- Configuration Guide

### Tests
Multiple test suites ensuring reliability:
- Unit tests (`tests/`)
- Integration tests (`test/`)
- Browser-specific tests
- Core functionality tests

### Configuration
Various configuration options through:
- Environment variables
- YAML configuration files
- Constructor parameters
- Project-level settings

## Directory Layout

```
nova-act/
├── src/
│   ├── nova_act/        # Python SDK implementation
│   └── frontend/        # Web UI implementation
├── main/
│   └── java/           # Java SDK implementation
├── docs/               # Documentation
├── tests/             # Test suites
├── configs/           # Configuration templates
└── yamls/            # YAML definitions and schemas
```

## Getting Started

Most users should begin with the Python SDK, which is the primary and most feature-complete implementation. See the [Getting Started Guide](getting-started.md) for installation and basic usage instructions.

For enterprise Java applications, the Java SDK provides a native interface while maintaining feature parity with the Python implementation.

The web frontend is particularly useful for teams that need visual monitoring and control of Nova ACT operations.