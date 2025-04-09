"""Bridge module for NovaAct."""

from typing import Optional, Dict, Any


class NovaActBridge:
    """Bridge class for NovaAct communication."""

    def __init__(self):
        """Initialize the NovaActBridge."""
        self._connected: bool = False
        self._config: Optional[Dict[str, Any]] = None

    async def connect(self) -> None:
        """Connect to the Nova ACT bridge."""
        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect from the Nova ACT bridge."""
        self._connected = False

    @property
    def connected(self) -> bool:
        """Return True if connected to the bridge."""
        return self._connected


__all__ = ["NovaActBridge"]
