"""Bridge module for Nova ACT."""

import asyncio
import logging
from typing import Any, Dict, Optional

from nova_act.bridge.client import BridgeClient

__all__ = ["NovaActBridge", "BridgeClient"]

_LOGGER = logging.getLogger(__name__)


class NovaActBridge:
    """Bridge class for NovaAct communication with WebSocket server."""

    def __init__(self, host: str = "localhost", port: int = 8081):
        """Initialize the NovaActBridge.

        Args:
            host: Host address for the WebSocket server
            port: Port for the WebSocket server
        """
        self._host = host
        self._port = port
        self._connected: bool = False
        self._config: Optional[Dict[str, Any]] = None
        self._server_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the bridge server."""
        from nova_act.bridge.server import app
        import uvicorn

        try:
            config = uvicorn.Config(
                app=app, host=self._host, port=self._port, log_level="info"
            )
            server = uvicorn.Server(config)
            self._connected = True
            await server.serve()
        except Exception as e:
            _LOGGER.error(f"Failed to start bridge server: {e}")
            self._connected = False
            raise

    async def stop(self) -> None:
        """Stop the bridge server."""
        self._connected = False
        if self._server_task:
            self._server_task.cancel()
            try:
                await self._server_task
            except asyncio.CancelledError:
                pass
            self._server_task = None

    async def send_thought_update(self, thought_data: Dict[str, Any]) -> None:
        """Send a thought update through the bridge.

        Args:
            thought_data: The thought data to send
        """
        if not self._connected:
            _LOGGER.warning("Cannot send thought update: Bridge not connected")
            return

        # This would use the API to post the thought
        # In a real implementation, we'd use aiohttp or httpx to make a POST request
        _LOGGER.info(f"Sending thought update: {thought_data}")

    @property
    def connected(self) -> bool:
        """Return True if connected to the bridge."""
        return self._connected
