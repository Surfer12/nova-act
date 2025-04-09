# Nova Act: A Browser Automation SDK for Reliable Web Actions

Nova Act is a powerful Python/Java SDK that enables reliable browser automation by breaking down complex web workflows into natural language commands. It combines the precision of Playwright with an intelligent agent to handle dynamic web interactions while providing a simple, intuitive API.

The SDK allows developers to automate web interactions using natural language commands while maintaining fine-grained control through Python/Java code. It features a WebSocket bridge for real-time updates, comprehensive logging, and support for both headless and headed browser automation. The SDK is particularly useful for automating complex web workflows, testing web applications, and building web automation tools.

Key features include:
- Natural language command interface for browser automation
- Built on Playwright for reliable web automation
- Real-time updates via WebSocket bridge
- Comprehensive logging and debugging capabilities
- Support for both Python and Java
- Configurable screen dimensions and Chrome channels
- Video recording capabilities
- Session management with user data directories
- Extension-based architecture for extensibility

## Repository Structure
```
nova-act/
├── src/                    # Source code directory
│   ├── nova_act/          # Core Python implementation
│   │   ├── bridge/        # WebSocket bridge implementation
│   │   ├── impl/         # Core implementation modules
│   │   ├── samples/      # Example implementations
│   │   └── types/        # Type definitions and schemas
│   └── frontend/         # React-based frontend implementation
├── main/                  # Java implementation
│   └── java/com/amazon/novaact/
├── test/                  # Test directories for Java
└── tests/                # Test directories for Python
```

## Usage Instructions
### Prerequisites
- Python 3.12 or higher
- Java 21 or higher (for Java implementation)
- Node.js and npm (for frontend development)
- Chrome browser installed
- Playwright browser automation framework

For C++ compiler requirements:
- MacOS: Xcode Command Line Tools
- Linux: GCC/G++ 11 or higher
- Windows: Visual Studio 2019 or higher with C++ workload

### Installation

#### Python Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

#### Java Installation
```bash
# Build with Maven
mvn clean install
```

### Quick Start
```python
from nova_act import NovaAct

# Initialize NovaAct with starting page
nova = NovaAct(starting_page="https://www.google.com")

# Start the browser
nova.start()

# Execute natural language command
result = nova.act("search for 'python programming'")

# Close the browser
nova.stop()
```

### More Detailed Examples

1. Order a salad from Sweetgreen:
```python
from nova_act import NovaAct

async def order_salad():
    with NovaAct(
        starting_page="https://order.sweetgreen.com",
        headless=False
    ) as nova:
        await nova.act(
            "Click Menu at the top of the page. "
            "Click Delivery on the sidebar. "
            "Select 'Home' address. "
            "Scroll down and click on 'Shroomami'. "
            "Click 'Add to Bag'."
        )
```

2. Search for apartments near Caltrain:
```python
from nova_act import NovaAct

async def find_apartments():
    nova = NovaAct(
        starting_page="https://www.realestate-website.com/",
        headless=True
    )
    await nova.start()
    await nova.act("search for apartments in Redwood City")
    listings = await nova.act("extract 5 apartment listings")
```

### Troubleshooting

Common Issues:

1. Browser Launch Fails
```
Error: Failed to launch browser
Solution: 
- Ensure Chrome is installed
- Check if the specified Chrome channel is available
- Verify user permissions for browser access
```

2. WebSocket Connection Issues
```
Error: WebSocket connection failed
Solution:
- Check if the bridge server is running (default: localhost:8081)
- Verify network connectivity
- Check firewall settings
```

3. Extension Loading Issues
```
Error: Failed to load extension
Solution:
- Verify extension path is correct
- Ensure extension is properly compiled
- Check Chrome version compatibility
```

Debugging:
- Enable debug logging:
```python
nova = NovaAct(
    starting_page="https://example.com",
    logs_directory="/path/to/logs",
    debug=True
)
```
- Log files location: `/path/to/logs/nova_act_*.log`
- Enable verbose logging in config.json:
```json
{
    "logging": {
        "level": "debug",
        "console": true
    }
}
```

## Data Flow
Nova Act processes commands through a multi-stage pipeline that transforms natural language into browser actions.

```
[User Command] -> [NovaAct Client] -> [Bridge Server] -> [Extension]
       ^                                                      |
       |                                                      v
[Result/Updates] <- [WebSocket Bridge] <- [Browser Actions] <- [Playwright]
```

Component interactions:
1. User submits natural language command to NovaAct client
2. Command is processed and sent to Bridge Server via WebSocket
3. Bridge Server forwards command to Chrome Extension
4. Extension uses Playwright to execute browser actions
5. Results and updates are sent back through WebSocket bridge
6. Real-time updates are provided to the client
7. Final results are returned to the user
8. Error handling and retries occur at each stage