"""Bridge server implementation."""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, Optional

from aiohttp import web
from websockets.legacy.server import WebSocketServerProtocol

from ..util.logging import setup_logging
from .exceptions import MessageError

_LOGGER = setup_logging(__name__)


class NovaBridgeServer:
    """Server for Nova Bridge service."""

    def __init__(self, host: str = "localhost", port: int = 8081):
        """Initialize server.

        Args:
            host: Host to bind server to
            port: Port to listen on
        """
        self.host = host
        self.port = port
        self.app = web.Application()
        self.websocket_handler = None
        self._setup_routes()

    def _setup_routes(self):
        """Set up HTTP routes."""
        self.app.router.add_post("/thought", self._handle_thought)
        self.app.router.add_post("/intervention", self._handle_intervention)
        self.app.router.add_get("/ws", self._handle_websocket)

    async def _handle_thought(self, request: web.Request) -> web.Response:
        """Handle thought endpoint."""
        data = await request.json()
        return web.json_response({"status": "ok"})

    async def _handle_intervention(self, request: web.Request) -> web.Response:
        """Handle intervention endpoint."""
        data = await request.json()
        return web.json_response({"status": "ok"})

    async def _handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        return ws

    async def start(self):
        """Start the bridge server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        _LOGGER.info(f"Bridge server started on http://{self.host}:{self.port}")

    async def stop(self):
        """Stop the bridge server."""
        await self.app.shutdown()
        _LOGGER.info("Bridge server stopped")
