import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from nova_act.util.logging import setup_logging

_LOGGER = setup_logging(__name__)

app = FastAPI(title="Nova Act Bridge Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for thoughts and interventions
thoughts: List[Dict[str, Any]] = []
interventions: List[Dict[str, Any]] = []


class ThoughtUpdate(BaseModel):
    """Model for thought update requests."""

    sessionId: str = Field(..., description="Unique session identifier")
    initialState: str = Field(..., description="Initial state of the thought")
    recursiveElaboration: str = Field(..., description="Recursive elaboration of the thought")
    transformativeInput: str = Field(..., description="Transformative input applied")
    emergentPattern: str = Field(..., description="Emergent pattern observed")
    processingLevel: str = Field(..., description="Level of processing")
    iterationCount: int = Field(..., ge=1, description="Number of iterations")


class InterventionUpdate(BaseModel):
    """Model for intervention update requests."""

    sessionId: str = Field(..., description="Unique session identifier")
    type: str = Field(..., description="Type of intervention")
    content: str = Field(..., description="Intervention content")
    targetThought: Optional[str] = Field(None, description="Target thought identifier")
    processingLevel: str = Field(..., description="Level of processing")


class ConnectionManager:
    """Manages WebSocket connections and message broadcasting."""

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection to accept
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        _LOGGER.info(
            f"New WebSocket connection accepted. Total connections: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove a WebSocket connection.

        Args:
            websocket: The WebSocket connection to remove
        """
        try:
            self.active_connections.remove(websocket)
            _LOGGER.info(
                f"WebSocket connection removed. Total connections: {len(self.active_connections)}"
            )
        except ValueError:
            _LOGGER.warning("Attempted to remove non-existent WebSocket connection")

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """
        Broadcast a message to all connected clients.

        Args:
            message: The message to broadcast
        """
        disconnected: List[WebSocket] = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                _LOGGER.error(f"Error sending message: {e}")
                disconnected.append(connection)

        # Clean up failed connections
        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


@app.get("/api/thoughts")
async def get_thoughts() -> List[Dict[str, Any]]:
    """Get all recorded thoughts."""
    return thoughts


@app.post("/api/thoughts")
async def create_thought(thought: ThoughtUpdate) -> Dict[str, Any]:
    """
    Create a new thought and broadcast it.

    Args:
        thought: The thought data to create

    Returns:
        Dict containing the created thought data
    """
    thought_dict = thought.dict()
    thought_dict["id"] = str(uuid4())
    thought_dict["timestamp"] = datetime.now().isoformat()
    thoughts.append(thought_dict)

    # Broadcast to WebSocket clients
    await manager.broadcast({"eventType": "thoughtUpdate", "data": thought_dict})

    return thought_dict


@app.get("/api/interventions")
async def get_interventions() -> List[Dict[str, Any]]:
    """Get all recorded interventions."""
    return interventions


@app.post("/api/interventions")
async def create_intervention(intervention: InterventionUpdate) -> Dict[str, Any]:
    """
    Create a new intervention and broadcast it.

    Args:
        intervention: The intervention data to create

    Returns:
        Dict containing the created intervention data

    Raises:
        HTTPException: If the target thought doesn't exist
    """
    intervention_dict = intervention.dict()

    # Validate target thought if specified
    if intervention.targetThought and not any(
        t["id"] == intervention.targetThought for t in thoughts
    ):
        raise HTTPException(status_code=404, detail="Target thought not found")

    intervention_dict["id"] = str(uuid4())
    intervention_dict["timestamp"] = datetime.now().isoformat()
    interventions.append(intervention_dict)

    # Broadcast to WebSocket clients
    await manager.broadcast({"eventType": "interventionUpdate", "data": intervention_dict})

    return intervention_dict


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Handle WebSocket connections.

    Args:
        websocket: The WebSocket connection to handle
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse and validate the message
                json.loads(data)
                # Handle incoming WebSocket messages if needed
            except json.JSONDecodeError as e:
                _LOGGER.error(f"Invalid JSON received: {e}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        _LOGGER.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
