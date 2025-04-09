"""Bridge client implementation."""

import json
from typing import Any, Dict, Optional

import aiohttp

from ..util.logging import setup_logging
from .exceptions import ConnectionError

_LOGGER = setup_logging(__name__)


class BridgeClient:
    """Client for communicating with the Nova Bridge service."""

    def __init__(
        self,
        base_url: str = "http://localhost:8081",
        ws_url: str = "ws://localhost:8081/ws",
    ):
        """Initialize client.

        Args:
            base_url: Base URL of the bridge service
            ws_url: WebSocket URL for real-time communication
        """
        self.base_url = base_url
        self.ws_url = ws_url
        self.session = None
        self.ws = None

    async def connect(self):
        """Connect to the bridge service."""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close connection to bridge service."""
        if self.session:
            await self.session.close()
            self.session = None
