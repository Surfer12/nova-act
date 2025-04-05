import json
from typing import Any, Dict, Optional

import aiohttp

from nova_act.util.logging import setup_logging

_LOGGER = setup_logging(__name__)


class NovaBridgeClient:
    """Client for communicating with the Nova Bridge service."""

    def __init__(
        self, base_url: str = "http://localhost:8080", ws_url: str = "ws://localhost:8080/ws"
    ):
        self.base_url = base_url.rstrip("/")
        self.ws_url = ws_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None

    async def connect(self):
        """Initialize HTTP and WebSocket sessions."""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close HTTP and WebSocket sessions."""
        if self.ws:
            await self.ws.close()
            self.ws = None
        if self.session:
            await self.session.close()
            self.session = None

    async def publish_thought(
        self,
        session_id: str,
        initialState: str,
        recursiveElaboration: str,
        transformativeInput: str,
        emergentPattern: str,
        processingLevel: str,
        iterationCount: int,
    ) -> Dict[str, Any]:
        """Publish a thought update to the bridge."""
        if not self.session:
            await self.connect()

        thought_data = {
            "sessionId": session_id,
            "initialState": initialState,
            "recursiveElaboration": recursiveElaboration,
            "transformativeInput": transformativeInput,
            "emergentPattern": emergentPattern,
            "processingLevel": processingLevel,
            "iterationCount": iterationCount,
        }

        try:
            async with self.session.post(
                f"{self.base_url}/api/thoughts", json=thought_data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error(f"Failed to publish thought: {response.status}")
                    return {}
        except Exception as e:
            _LOGGER.error(f"Error publishing thought: {e}")
            return {}

    async def publish_intervention(
        self,
        session_id: str,
        type: str,
        content: str,
        targetThought: Optional[str] = None,
        processingLevel: str = "mesoLevel",
    ) -> Dict[str, Any]:
        """Publish an intervention to the bridge."""
        if not self.session:
            await self.connect()

        intervention_data = {
            "sessionId": session_id,
            "type": type,
            "content": content,
            "targetThought": targetThought,
            "processingLevel": processingLevel,
        }

        try:
            async with self.session.post(
                f"{self.base_url}/api/interventions", json=intervention_data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error(f"Failed to publish intervention: {response.status}")
                    return {}
        except Exception as e:
            _LOGGER.error(f"Error publishing intervention: {e}")
            return {}

    async def connect_websocket(self, on_message):
        """Connect to the WebSocket endpoint and set up message handler."""
        if not self.session:
            await self.connect()

        try:
            self.ws = await self.session.ws_connect(self.ws_url)
            _LOGGER.info("Connected to Nova Bridge WebSocket")

            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await on_message(data)
                    except json.JSONDecodeError:
                        _LOGGER.error(f"Invalid JSON received: {msg.data}")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    _LOGGER.error(f"WebSocket error: {msg.data}")
                    break
        except Exception as e:
            _LOGGER.error(f"WebSocket connection error: {e}")
            self.ws = None
