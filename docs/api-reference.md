# API Reference

## NovaAct Class

The main class for interacting with Nova ACT.

### Constructor

```python
NovaAct(
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
    nova_act_api_key: str | None = None,
    playwright_instance: Playwright | None = None,
    endpoint_name: str = "default",
    tty: bool = True,
    cdp_endpoint_url: str | None = None
) -> None
```

### Methods

#### start()

Start the Nova ACT client.

```python
def start(self) -> None
```

#### stop()

Stop the Nova ACT client.

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

### Properties

- `started: bool` - Whether the client has been started
- `pages: List[Page]` - List of active Playwright pages
- `dispatcher: ExtensionDispatcher` - The extension dispatcher for actuation

## Configuration

### Environment Variables

- `NOVA_ACT_API_KEY` - Your Nova ACT API key
- `NOVA_ACT_HEADLESS` - Whether to run in headless mode
- `NOVA_ACT_CHROME_CHANNEL` - Chrome channel to use

### Configuration Files

Configuration files should be in JSON format. Example:

```json
{
    "api_key": "your-api-key",
    "headless": false,
    "chrome_channel": "chrome"
}
``` 