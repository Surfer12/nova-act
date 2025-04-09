#!/usr/bin/env python
"""
Simple demonstration of nova-act functionality.
"""

import asyncio
import logging
import os
import sys

# Configure logging first
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add src to the path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Try to import from the core module first
try:
    from nova_act.core import NovaAct

    logger.info("Using core NovaAct implementation")
except ImportError:
    try:
        # Fall back to main implementation
        from nova_act import NovaAct

        logger.info("Using main NovaAct implementation")
    except ImportError:
        # Finally try the minimal implementation
        from nova_act.nova_act import NovaAct

        logger.info("Using minimal NovaAct implementation")


async def main():
    """Run a simple demonstration of nova-act."""
    logger.info("Starting nova-act demonstration")

    # Create a nova instance with core implementation
    nova = NovaAct(headless=False)

    try:
        # Start the browser
        logger.info("Starting browser")
        await nova.start()
        logger.info("Browser started")

        # Simulate some browser actions (since core implementation doesn't actually do anything)
        logger.info("Demonstrating browser actions")

        # In a real implementation, we'd be able to call methods like:
        # await nova.navigate("https://www.google.com")
        # await nova.act("Search for something")

        # Instead, let's check if we're connected to the bridge
        if hasattr(nova, "bridge") and nova.bridge:
            logger.info("Using bridge API")
            if hasattr(nova.bridge, "connected"):
                logger.info(f"Bridge connected: {nova.bridge.connected}")
            logger.info("Would use bridge API to control browser")
        else:
            logger.info("Using direct browser control API")
            logger.info("Would use direct API to control browser")

        # Wait to simulate browser being open
        logger.info("Browser will remain open for 5 seconds...")
        await asyncio.sleep(5)

    finally:
        # Clean up
        logger.info("Stopping browser...")

        # Use the available method - stop() or disconnect()
        if hasattr(nova, "stop") and callable(getattr(nova, "stop")):
            await nova.stop()
            logger.info("Browser stopped with nova.stop()")
        elif hasattr(nova, "disconnect") and callable(getattr(nova, "disconnect")):
            await nova.disconnect()
            logger.info("Browser stopped with nova.disconnect()")

    logger.info("Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
