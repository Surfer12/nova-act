"""Type stub for bridge package."""

from typing import Dict, Any, Awaitable

from aiohttp import web

from .bridge import NovaBridge
from .client import BridgeClient
from .server import NovaBridgeServer

async def websocket_handler(
    app: web.Application, request: web.Request
) -> web.WebSocketResponse: ...

__all__ = [
    "NovaBridge",
    "BridgeClient",
    "NovaBridgeServer",
    "websocket_handler",
]
