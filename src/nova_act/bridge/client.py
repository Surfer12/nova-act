"""Client module for bridge communication."""

import asyncio
import json
import logging
from typing import Any, Dict, Optional

import aiohttp

_LOGGER = logging.getLogger(__name__)


class BridgeClient:
    """Client for communicating with the Nova ACT bridge server."""

    def __init__(self, host: str = "localhost", port: int = 8081):
        """Initialize the bridge client.

        Args:
            host: Host address for the bridge server
            port: Port for the bridge server
        """
        self._host = host
        self._port = port
        self._base_url = f"http://{host}:{port}"
        self._connected = False
        self._session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> None:
        """Connect to the bridge server."""
        if self._connected:
            return

        self._session = aiohttp.ClientSession()
        self._connected = True
        _LOGGER.info(f"Connected to bridge server at {self._base_url}")

    async def disconnect(self) -> None:
        """Disconnect from the bridge server."""
        if not self._connected or not self._session:
            return

        await self._session.close()
        self._session = None
        self._connected = False
        _LOGGER.info("Disconnected from bridge server")

    async def get_thoughts(self) -> Dict[str, Any]:
        """Get all thoughts from the bridge server.

        Returns:
            Dict[str, Any]: The thoughts from the bridge server
        """
        if not self._connected or not self._session:
            raise RuntimeError("Not connected to bridge server")

        async with self._session.get(f"{self._base_url}/api/thoughts") as response:
            response.raise_for_status()
            return await response.json()

    async def create_thought(self, thought_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new thought on the bridge server.

        Args:
            thought_data: The thought data to create

        Returns:
            Dict[str, Any]: The created thought data
        """
        if not self._connected or not self._session:
            raise RuntimeError("Not connected to bridge server")

        async with self._session.post(
            f"{self._base_url}/api/thoughts", json=thought_data
        ) as response:
            response.raise_for_status()
            return await response.json()

    @property
    def connected(self) -> bool:
        """Return True if connected to the bridge server."""
        return self._connected
