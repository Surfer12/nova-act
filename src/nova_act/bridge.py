import json
import asyncio
import websockets
from typing import Any, Dict, Optional
from nova_act.util.logging import setup_logging

_LOGGER = setup_logging(__name__)

class NovaActBridge:
    """WebSocket bridge for Nova Act to communicate with frontend."""
    
    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        
    async def start(self):
        """Start the WebSocket server."""
        self.server = await websockets.serve(
            self._handle_client,
            self.host,
            self.port
        )
        _LOGGER.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        
    async def stop(self):
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            _LOGGER.info("WebSocket server stopped")
            
    async def _handle_client(self, websocket, path):
        """Handle new WebSocket client connections."""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    _LOGGER.debug(f"Received message: {data}")
                    # Handle incoming messages from frontend if needed
                except json.JSONDecodeError:
                    _LOGGER.error(f"Invalid JSON received: {message}")
        finally:
            self.clients.remove(websocket)
            
    async def broadcast(self, message_type: str, data: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        if not self.clients:
            return
            
        message = {
            "type": message_type,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        message_json = json.dumps(message)
        websockets.broadcast(self.clients, message_json)
        _LOGGER.debug(f"Broadcast message: {message}")
        
    async def send_thought_update(self, thought_data: Dict[str, Any]):
        """Send a thought update to connected clients."""
        await self.broadcast("thoughtUpdate", thought_data)
        
    async def send_meta_intervention(self, intervention_data: Dict[str, Any]):
        """Send a meta-intervention update to connected clients."""
        await self.broadcast("metaIntervention", intervention_data) 