from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nova_act import NovaAct
from nova_act.bridge import Bridge, BridgeMessage

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store NovaAct instances by session ID
nova_act_instances: Dict[str, NovaAct] = {}

class NovaActConfig(BaseModel):
    environment: str = "development"
    logging: Dict[str, str] = {"level": "info"}
    browser: Dict[str, Any] = {
        "starting_page": "https://www.google.com",
        "headless": True,
        "chrome_channel": "chrome",
        "screen_width": 1920,
        "screen_height": 1080,
    }

class NovaActRequest(BaseModel):
    session_id: str
    action: str
    params: Optional[Dict[str, Any]] = None

@app.post("/init")
async def init_nova_act(config: NovaActConfig, session_id: str):
    try:
        instance = NovaAct(config=config.dict())
        nova_act_instances[session_id] = instance
        return {"status": "success", "message": "NovaAct initialized"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/act")
async def act(request: NovaActRequest):
    if request.session_id not in nova_act_instances:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        instance = nova_act_instances[request.session_id]
        result = await instance.act(request.action, request.params or {})
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start")
async def start(session_id: str):
    if session_id not in nova_act_instances:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        instance = nova_act_instances[session_id]
        await instance.start()
        return {"status": "success", "message": "NovaAct started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop")
async def stop(session_id: str):
    if session_id not in nova_act_instances:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        instance = nova_act_instances[session_id]
        await instance.stop()
        return {"status": "success", "message": "NovaAct stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 