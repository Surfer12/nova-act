"""Type stubs for nova_act."""

from typing import Dict, Any

from nova_act.bridge.bridge import NovaBridge
from nova_act.bridge.client import BridgeClient
from nova_act.bridge.server import NovaBridgeServer
from nova_act.nova_act import NovaAct
from nova_act.types.act_result import ActResult
from nova_act.util.logging import setup_logging

def load_config(config_path: str) -> Dict[str, Any]: ...

__version__: str

__all__ = [
    "load_config",
    "setup_logging",
    "NovaAct",
    "BridgeClient",
    "NovaBridgeServer",
    "NovaBridge",
    "ActResult",
]
