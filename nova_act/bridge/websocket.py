"""WebSocket support module."""
from aiohttp import web

from ..util.logging import setup_logging

_LOGGER = setup_logging(__name__)

async def websocket_handler(app: web.Application, request: web.Request) -> web.WebSocketResponse:
    """Handle WebSocket connections.
    
    Args:
        app: The aiohttp application
        request: The HTTP request
        
    Returns:
        WebSocket response object
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    _LOGGER.info("WebSocket client connected")
    return ws