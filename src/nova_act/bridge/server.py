import json
import uuid
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nova_act.util.logging import setup_logging

_LOGGER = setup_logging(__name__)

app = FastAPI()

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


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                _LOGGER.error(f"Error sending message: {e}")
                self.disconnect(connection)


manager = ConnectionManager()


# Pydantic models for request validation
class ThoughtUpdate(BaseModel):
    sessionId: str
    initialState: str
    recursiveElaboration: str
    transformativeInput: str
    emergentPattern: str
    processingLevel: str
    iterationCount: int


class InterventionUpdate(BaseModel):
    sessionId: str
    type: str
    content: str
    targetThought: str | None = None
    processingLevel: str


# REST endpoints
@app.get("/api/thoughts")
async def get_thoughts():
    return thoughts


@app.post("/api/thoughts")
async def create_thought(thought: ThoughtUpdate):
    thought_dict = thought.dict()
    thought_dict["id"] = str(uuid.uuid4())
    thought_dict["timestamp"] = datetime.now().isoformat()
    thoughts.append(thought_dict)

    # Broadcast to WebSocket clients
    await manager.broadcast({"eventType": "thoughtUpdate", "data": thought_dict})

    return thought_dict


@app.get("/api/interventions")
async def get_interventions():
    return interventions


@app.post("/api/interventions")
async def create_intervention(intervention: InterventionUpdate):
    intervention_dict = intervention.dict()
    intervention_dict["id"] = str(uuid.uuid4())
    intervention_dict["timestamp"] = datetime.now().isoformat()
    interventions.append(intervention_dict)

    # Broadcast to WebSocket clients
    await manager.broadcast({"eventType": "interventionUpdate", "data": intervention_dict})

    return intervention_dict


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse the message but don't store it since it's not used
                json.loads(data)
                # Handle incoming WebSocket messages if needed
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
