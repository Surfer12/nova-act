import asyncio
import logging
from typing import Optional
import websockets
from websockets.server import WebSocketServerProtocol
from websockets.legacy.server import serve

class NovaActBridge:
    """Bridge for handling WebSocket connections in Nova Act."""
    
    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.server: Optional[websockets.server.WebSocketServer] = None
        self.clients: set[WebSocketServerProtocol] = set()
        self.logger = logging.getLogger(__name__)

    async def handle_client(self, websocket: WebSocketServerProtocol):
        """Handle individual WebSocket client connections."""
        self.clients.add(websocket)
        self.logger.info(f"New client connected. Total clients: {len(self.clients)}")
        
        try:
            async for message in websocket:
                # Handle incoming messages
                self.logger.debug(f"Received message: {message}")
                # Echo the message back to the client
                await websocket.send(f"Echo: {message}")
        except websockets.exceptions.ConnectionClosed:
            self.logger.info("Client connection closed")
        finally:
            self.clients.remove(websocket)
            self.logger.info(f"Client disconnected. Remaining clients: {len(self.clients)}")

    async def start(self):
        """Start the WebSocket server."""
        self.server = await serve(
            self.handle_client,
            self.host,
            self.port,
            process_request=self.process_request
        )
        self.logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")

    async def stop(self):
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.logger.info("WebSocket server stopped")
            
    async def process_request(self, path, headers):
        """Custom request processor that's more lenient with headers."""
        return None  # None means the connection is accepted 