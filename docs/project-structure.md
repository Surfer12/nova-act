# Nova ACT Project Structure

This document explains the organization of the Nova ACT project and provides recommendations for maintaining a clean project structure.

## Current Project Organization

Nova ACT currently has the following structure:

```
nova-act/
├── docs/                         # Documentation
│   ├── api-reference.md
│   ├── examples.md
│   ├── getting-started.md
│   ├── index.md
│   └── project-structure.md      # This file
├── nova_act/                     # Redundant Python package (to be removed)
│   ├── __init__.py
│   ├── __init__.pyi
│   ├── bridge/
│   ├── cli/
│   ├── nova_act.py               # Simplified implementation (635B)
│   ├── py.typed
│   ├── types/
│   └── util/
├── src/
│   ├── frontend/                 # React TypeScript web application
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── src/
│   │   └── ...
│   └── nova_act/                 # Primary Python SDK
│       ├── __init__.py
│       ├── __version__.py
│       ├── bridge/
│       ├── cli/
│       ├── impl/
│       ├── main.py
│       ├── nova_act.py           # Full implementation (19KB)
│       ├── py.typed
│       ├── samples/
│       ├── types/
│       └── util/
└── main/
    └── java/                     # Java SDK
        └── com/
            └── amazon/
                └── novaact/
```

## Component Descriptions

Nova ACT consists of three primary components:

1. **Python SDK** (`src/nova_act/`):
   - Full-featured Python implementation
   - Documented in the API reference
   - Primary focus of the examples and documentation

2. **Java SDK** (`main/java/com/amazon/novaact/`):
   - Java implementation for use in Java applications
   - JVM-based interface to Nova ACT functionality

3. **Web Frontend** (`src/frontend/`):
   - React TypeScript web application
   - Likely provides a browser-based interface

## Known Issues and Recommendations

### 1. Redundant Python Implementation

The `nova_act/` directory at the project root contains a simplified, outdated implementation that is redundant with the primary implementation in `src/nova_act/`.

**Recommendation**: Remove the redundant `nova_act/` directory at the root level:

```bash
# Backup first (optional)
cp -r nova_act nova_act_backup

# Remove the redundant directory
rm -rf nova_act
```

### 2. Improved Structure

For better organization, consider restructuring the project as follows:

```
nova-act/
├── docs/                         # Documentation
├── python/                       # Python SDK (move from src/nova_act/)
├── java/                         # Java SDK (move from main/java/)
├── web/                          # Web frontend (move from src/frontend/)
└── README.md
```

This restructuring would:
- Clearly separate the different implementations
- Make it easier to understand the project components
- Improve maintainability

## Implementation Notes

### Python SDK (`src/nova_act/`)

The primary Python SDK provides:
- Comprehensive API for web automation
- Integration with Playwright for browser control
- Error handling and recovery mechanisms
- Schema validation for structured data extraction

### Java SDK (`main/java/com/amazon/novaact/`)

The Java SDK likely:
- Provides similar functionality to the Python SDK
- Is packaged as a Java library
- Has Java-specific documentation

### Web Frontend (`src/frontend/`)

The React application:
- Provides a browser-based UI for Nova ACT
- Written in TypeScript
- Uses React components

## Documentation References

The documentation has been updated to reference the primary Python SDK in `src/nova_act/`:

- [Index](index.md) - Overview and features
- [Getting Started](getting-started.md) - Installation and basic usage
- [API Reference](api-reference.md) - Detailed API documentation
- [Examples](examples.md) - Usage examples 