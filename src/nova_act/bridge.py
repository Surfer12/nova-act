import json
import asyncio
import websockets
from typing import Any, Dict, Optional, List
from nova_act.util.logging import setup_logging
import uuid

_LOGGER = setup_logging(__name__)

class NovaActBridge:
    """WebSocket bridge for Nova Act to communicate with frontend."""
    
    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        self.fractal_config = None
        
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
                    
                    # Handle Fractal Explorer specific messages
                    if data.get("type") == "FRACTAL_CONFIG":
                        self.fractal_config = data.get("config")
                        await self.broadcast("fractalConfigAck", {"status": "received"})
                    elif data.get("type") == "META_INTERVENTION":
                        await self.handle_meta_intervention(data.get("intervention"))
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
        # Transform thought data according to fractal config if available
        if self.fractal_config:
            thought_data = self._transform_thought_for_fractal(thought_data)
        await self.broadcast("thoughtUpdate", thought_data)
        
    async def send_meta_intervention(self, intervention_data: Dict[str, Any]):
        """Send a meta-intervention update to connected clients."""
        await self.broadcast("metaIntervention", intervention_data)
        
    def _transform_thought_for_fractal(self, thought_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform thought data according to fractal configuration."""
        # Apply fractal transformation rules from config
        transformed = {
            "id": thought_data.get("id", str(uuid.uuid4())),
            "prompt": thought_data.get("prompt"),
            "result": thought_data.get("result"),
            "metadata": thought_data.get("metadata", {}),
            "fractalData": {
                "level": thought_data.get("processingLevel", "mesoLevel"),
                "iteration": thought_data.get("iterationCount", 1),
                "timestamp": thought_data.get("timestamp"),
                "transformations": self._apply_fractal_transformations(thought_data)
            }
        }
        return transformed
        
    def _apply_fractal_transformations(self, thought_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply fractal transformations based on config."""
        transformations = []
        if self.fractal_config:
            # Apply transformations defined in fractal config
            for transform in self.fractal_config.get("transformations", []):
                if transform.get("condition")(thought_data):
                    transformations.append({
                        "type": transform.get("type"),
                        "params": transform.get("params"),
                        "result": transform.get("transform")(thought_data)
                    })
        return transformations 