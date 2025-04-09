#!/usr/bin/env python
"""
Demonstration of connecting to the Nova ACT bridge.
"""

import asyncio
import logging
import sys
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add src to path to ensure correct imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import bridge client
try:
    from nova_act.bridge.client import BridgeClient
    logger.info("Successfully imported BridgeClient")
except ImportError as e:
    logger.error(f"Failed to import BridgeClient: {e}")
    sys.exit(1)


async def main():
    """Connect to the Nova ACT bridge and demonstrate functionality."""
    # Create bridge client
    client = BridgeClient(host="127.0.0.1", port=8082)
    
    try:
        # Connect to bridge
        logger.info("Connecting to Nova ACT bridge...")
        await client.connect()
        logger.info(f"Connected: {client.connected}")
        
        # Get thoughts
        try:
            logger.info("Fetching thoughts from bridge...")
            thoughts = await client.get_thoughts()
            logger.info(f"Retrieved {len(thoughts) if isinstance(thoughts, list) else 'unknown'} thoughts")
            logger.info(f"Thoughts: {json.dumps(thoughts, indent=2)}")
        except Exception as e:
            logger.error(f"Error fetching thoughts: {e}")
        
        # Create a thought
        try:
            logger.info("Creating a new thought...")
            # Use the proper format according to ThoughtUpdate model in server.py
            thought_data = {
                "sessionId": "example-session-123",
                "initialState": "Example thought from bridge client",
                "recursiveElaboration": "Exploring the functionality of the bridge client",
                "transformativeInput": "Additional context from the example script",
                "emergentPattern": "This is a test thought from the bridge client example",
                "processingLevel": "demo",
                "iterationCount": 1
            }
            response = await client.create_thought(thought_data)
            logger.info(f"Create thought response: {json.dumps(response, indent=2)}")
        except Exception as e:
            logger.error(f"Error creating thought: {e}")
        
        # Wait a moment
        logger.info("Waiting 2 seconds...")
        await asyncio.sleep(2)
        
    finally:
        # Disconnect from bridge
        logger.info("Disconnecting from bridge...")
        await client.disconnect()
        logger.info("Disconnected")


if __name__ == "__main__":
    asyncio.run(main())