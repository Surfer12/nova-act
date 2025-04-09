"""Bridge implementation module."""

import asyncio
import json
import uuid
from typing import Any, Dict, List, Optional, Set

from aiohttp import web
from websockets.legacy.server import WebSocketServerProtocol

from ..util.logging import setup_logging

_LOGGER = setup_logging(__name__)


class NovaBridge:
    """Bridge for Nova ACT to communicate with frontend."""

    def __init__(self, host: str = "localhost", port: int = 8081) -> None:
        """Initialize bridge."""
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()

    async def broadcast(self, message_type: str, data: Dict[str, Any]) -> None:
        """Broadcast a message to all connected clients."""
        if not self.clients:
            return

        try:
            message = {"type": message_type, "data": data}
            message_json = json.dumps(message)
            _LOGGER.debug(f"Broadcasting message: {message}")

            for client in self.clients:
                try:
                    await client.send(message_json)
                except Exception as e:
                    _LOGGER.error(f"Failed to send message to client: {e}")
                    self.clients.remove(client)
        except Exception as e:
            _LOGGER.error(f"Failed to broadcast message: {e}")
