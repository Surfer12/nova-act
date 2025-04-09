import asyncio
import logging
from typing import Optional
import websockets
from websockets.client import WebSocketClientProtocol


class BridgeClient:
    """Client for connecting to the Nova Act Bridge."""

    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """Connect to the WebSocket server."""
        uri = f"ws://{self.host}:{self.port}"
        self.websocket = await websockets.connect(uri)
        self.logger.info(f"Connected to WebSocket server at {uri}")

    async def send_message(self, message: str) -> str:
        """Send a message to the server and wait for response."""
        if not self.websocket:
            raise RuntimeError("Not connected to server. Call connect() first.")
        
        await self.websocket.send(message)
        response = await self.websocket.recv()
        self.logger.debug(f"Sent message: {message}, Received response: {response}")
        return response

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.logger.info("Disconnected from WebSocket server") 