# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Nova ACT Framework."""

import json
import os
from typing import Any, Dict, Optional

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict containing the configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is not valid JSON
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        return json.load(f)

# Initialize logging and core utilities
from .util.logging import setup_logging

_LOGGER = setup_logging(__name__)

# Import types
from .types.act_result import ActResult
from .types.typing import JsonDict, MessageHandler, OptionalDict

# Import core implementations
from .nova_act import NovaAct

# Import bridge components after NovaAct to avoid circular imports
from .bridge.bridge import NovaBridge
from .bridge.client import BridgeClient
from .bridge.server import NovaBridgeServer


# Version of the nova_act package
__version__ = "0.1.0"

# Export public API
__all__ = [
    'load_config',
    'setup_logging', 
    'NovaAct',
    'BridgeClient',
    'NovaBridgeServer',
    'NovaBridge',
    'ActResult',
    '__version__'
]