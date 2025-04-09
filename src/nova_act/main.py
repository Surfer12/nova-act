import asyncio
import logging
import sys
from pathlib import Path

from nova_act.bridge import NovaActBridge

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Start the Nova Act WebSocket server."""
    bridge = NovaActBridge(host="localhost", port=8081)
    try:
        logger.info("Starting Nova Act WebSocket server...")
        await bridge.start()
        logger.info(f"Server running on ws://localhost:8081")

        # Keep the server running
        await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await bridge.stop()
    except Exception as e:
        logger.error(f"Error running server: {e}")
        await bridge.stop()


if __name__ == "__main__":
    asyncio.run(main())
