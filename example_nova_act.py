#!/usr/bin/env python
import asyncio
import logging
import os
import sys

# Add src to the path for imports
sys.path.insert(0, os.path.dirname(__file__))

from nova_act.core import NovaAct  # Import from the core module

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Simple example of using NovaAct with a minimal implementation
async def main():
    """Simple example using the core NovaAct class"""
    try:
        logger.info("Creating NovaAct instance...")
        nova = NovaAct(headless=True)
        logger.info("NovaAct instance created successfully")

        # Start the browser
        logger.info("Starting browser...")
        await nova.start()
        logger.info("Browser started successfully")

        # Wait a moment (simulating browser actions)
        logger.info("Simulating browser actions...")
        await asyncio.sleep(1)

        # Stop the browser
        logger.info("Stopping browser...")
        await nova.stop()
        logger.info("Browser stopped successfully")

        logger.info("Example completed successfully!")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
