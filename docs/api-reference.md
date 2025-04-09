# API Reference

This document provides detailed information about the Nova ACT Python SDK API, implemented in `src/nova_act/`.

## Project Structure

Nova ACT consists of multiple components:

1. **Python SDK** (`src/nova_act/`): This API reference documents this implementation
2. **Java SDK** (`main/java/com/amazon/novaact/`): For Java bindings, see the Java documentation
3. **Web Frontend** (`src/frontend/`): React web application

## NovaAct Class

The main class for interacting with Nova ACT. Provides methods for web automation and AI-driven actions.

### Constructor

```python
NovaAct(
    # Browser Configuration
    starting_page: str = "https://www.google.com",
    user_data_dir: str | None = None,
    clone_user_data_dir: bool = True,
    profile_directory: str | None = None,
    extension_path: str | None = None,
    logs_directory: str | None = None,
    screen_width: int = 1600,
    screen_height: int = 900,
    headless: bool = False,
    chrome_channel: str | None = None,
    
    # API Configuration
    nova_act_api_key: str | None = None,
    playwright_instance: Playwright | None = None,
    endpoint_name: str = "default",
    tty: bool = True,
    cdp_endpoint_url: str | None = None
) -> None
```

#### Parameters

- **Browser Configuration**
  - `starting_page`: Initial URL to load (default: "https://www.google.com")
  - `user_data_dir`: Directory for browser user data
  - `clone_user_data_dir`: Whether to clone the user data directory
  - `profile_directory`: Specific browser profile to use
  - `extension_path`: Path to browser extension
  - `logs_directory`: Directory for log files
  - `screen_width`: Browser window width (default: 1600)
  - `screen_height`: Browser window height (default: 900)
  - `headless`: Run browser in headless mode
  - `chrome_channel`: Chrome channel to use

- **API Configuration**
  - `nova_act_api_key`: Your Nova ACT API key
  - `playwright_instance`: Custom Playwright instance
  - `endpoint_name`: API endpoint name
  - `tty`: Enable TTY mode
  - `cdp_endpoint_url`: Custom CDP endpoint URL

### Methods

#### start()

Start the Nova ACT client. Must be called before performing any actions.

```python
def start(self) -> None
```

#### stop()

Stop the Nova ACT client and clean up resources.

```python
def stop(self) -> None
```

#### act()

Perform an action using Nova ACT.

```python
def act(
    self,
    prompt: str,
    timeout: float | None = None,
    max_steps: int = 30,
    schema: Dict[str, Any] | None = None
) -> ActResult
```

##### Parameters

- `prompt`: The action to perform (e.g., "search for python programming")
- `timeout`: Maximum time to wait for action completion (in seconds)
- `max_steps`: Maximum number of steps to attempt
- `schema`: JSON schema for response validation

##### Returns

- `ActResult`: Object containing the action result and metadata

### Properties

- `started: bool` - Whether the client has been started
- `pages: List[Page]` - List of active Playwright pages
- `dispatcher: ExtensionDispatcher` - The extension dispatcher for actuation

## Configuration

### Environment Variables

```bash
# Required
export NOVA_ACT_API_KEY="your-api-key"

# Optional
export NOVA_ACT_HEADLESS="true"
export NOVA_ACT_CHROME_CHANNEL="chrome"
export NOVA_ACT_SCREEN_WIDTH="1920"
export NOVA_ACT_SCREEN_HEIGHT="1080"
```

### Configuration Files

Create a `nova_act_config.json` file:

```json
{
    "api_key": "your-api-key",
    "headless": false,
    "chrome_channel": "chrome",
    "screen_width": 1920,
    "screen_height": 1080,
    "user_data_dir": "/path/to/user/data",
    "profile_directory": "Profile 1"
}
```

## Error Handling

Nova ACT provides specific exception types for error handling:

```python
from nova_act.types.errors import StartFailed, StopFailed, ActFailed

try:
    with NovaAct() as nova:
        result = nova.act("perform action")
except StartFailed as e:
    print(f"Failed to start: {e}")
except StopFailed as e:
    print(f"Failed to stop: {e}")
except ActFailed as e:
    print(f"Action failed: {e}")
```

## Response Schema

The `ActResult` object contains:

```python
class ActResult:
    success: bool
    response: str
    error: str | None
    steps: List[Step]
    duration: float
    matches_schema: bool
    parsed_response: Any
```

See [Examples](examples.md) for more usage patterns. 