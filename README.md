# Nova Act: AI-Powered Web Browser Automation Framework

Nova Act is a Python framework that enables natural language-driven web browser automation, combining the power of AI with precise browser control to automate complex web interactions through simple English commands.

The framework provides a high-level interface for automating web tasks through natural language instructions while handling complex browser interactions, state management, and error recovery behind the scenes. It uses Playwright for browser automation and includes specialized analyzers for processing structured data like weather forecasts and renewable energy data.

Key features include:
- Natural language command interface for browser automation
- Built-in error handling and recovery mechanisms
- Support for headless operation
- Specialized data extraction and analysis capabilities
- Chrome extension integration for enhanced browser control
- Session management and logging
- Video recording capabilities
- Cross-platform support (MacOS, Linux, Windows)

## Repository Structure
```
nova_act/
├── impl/                   # Core implementation modules
│   ├── backend.py         # Backend service integration
│   ├── extension.py       # Chrome extension interface
│   ├── playwright.py      # Browser automation core
│   └── winguru_analyzer.py # Specialized wind data analyzer
├── samples/               # Example automation scripts
│   ├── analyze_winguru.py # Wind forecast analysis
│   ├── order_salad.py    # Food ordering automation
│   └── renewable_energy_forecast.py # Energy data analysis
├── types/                 # Type definitions and schemas
│   ├── act_errors.py     # Error type definitions
│   └── state/            # State management types
└── util/                 # Utility functions
    ├── jsonschema.py     # JSON schema validation
    └── logging.py        # Logging configuration
```

## Usage Instructions
### Prerequisites
- Python 3.13 or higher
- Chrome browser installed
- Playwright browser automation framework
- Required Python packages:
  - cryptography
  - fire
  - playwright==1.48.0
  - pydantic>=2.10.6
  - requests
  - retry
  - jsonschema
  - pandas
  - pillow

### Installation
1. Install the package using pip:
```bash
pip install nova-act
```

2. Install browser dependencies:
```bash
python -m playwright install chrome
```

3. Set up environment variables:
```bash
export NOVA_ACT_API_KEY=your_api_key
```

### Quick Start
```python
from nova_act import NovaAct

# Initialize the client
nova = NovaAct(starting_page="https://www.example.com")

# Start the browser
nova.start()

# Execute automation using natural language
result = nova.act("Click the login button and enter username 'user@example.com'")

# Close the browser
nova.stop()
```

### More Detailed Examples
1. Analyzing Wind Forecasts:
```python
from nova_act.samples.analyze_winguru import analyze_forecast

with NovaAct(starting_page="https://www.windguru.cz") as nova:
    forecast = analyze_forecast(nova)
    print(f"Wind conditions: {forecast.meta_analysis}")
```

2. Ordering Food:
```python
from nova_act.samples.order_salad import main

main(user_data_dir="~/chrome-data", order="Harvest Bowl")
```

### Troubleshooting
1. Browser Launch Issues
- Problem: Browser fails to launch
- Solution: Ensure Chrome is installed and accessible
```bash
# Check Chrome installation
which chrome
# Install Playwright dependencies
playwright install-deps
```

2. Authentication Errors
- Problem: "AuthError: Missing API key"
- Solution: Set the NOVA_ACT_API_KEY environment variable
```bash
export NOVA_ACT_API_KEY=your_api_key
```

3. Extension Loading Issues
- Problem: Chrome extension fails to load
- Solution: Verify extension path and permissions
```python
nova = NovaAct(
    starting_page="https://example.com",
    extension_path="/custom/path/to/extension"
)
```

## Data Flow
Nova Act processes automation commands through a pipeline that transforms natural language instructions into browser actions.

```ascii
[User Command] -> [NovaAct Client] -> [AI Processing] -> [Browser Actions]
     |                  |                   |                    |
     v                  v                   v                    v
Natural Language -> Command Parsing -> Action Planning -> Browser Automation
```

Key component interactions:
1. NovaAct client receives natural language commands
2. Commands are processed by the AI model for intent understanding
3. Playwright executes corresponding browser actions
4. Chrome extension provides additional browser control capabilities
5. Results and errors are captured and returned to the client
6. Specialized analyzers process structured data when needed
7. Session state is maintained throughout the automation flow