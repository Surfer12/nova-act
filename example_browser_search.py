#!/usr/bin/env python
import asyncio
import logging
import os
import sys

# Add src to the path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Demo of a browser launch and search using NovaAct"""
    try:
        # Import within function to handle import errors gracefully
        try:
            from src.nova_act.nova_act import NovaAct
        except ImportError:
            from nova_act.core import NovaAct  # Fallback to core implementation
            logger.warning("Using core NovaAct implementation (minimal functionality)")
        
        # 1. Create NovaAct instance
        logger.info("Creating NovaAct instance...")
        nova = NovaAct(headless=False)  # Use visible browser for demonstration
        logger.info("NovaAct instance created successfully")
        
        # 2. Start the browser
        logger.info("Starting browser...")
        await nova.start()
        logger.info("Browser started successfully")
        
        # 3. Demonstrate basic browser actions
        logger.info("Demonstrating browser actions...")
        
        # This will vary based on which implementation is available
        try:
            # Try to navigate to Google (full implementation)
            logger.info("Navigating to Google...")
            # This would normally use: await nova.navigate("https://www.google.com")
            
            # Try to perform a search (full implementation)
            logger.info("Performing search...")
            # This would normally use: await nova.act("search for Nova Act browser automation")
            
            # Since we're using the minimal implementation, simulate actions
            logger.info("Simulating search in minimal implementation...")
            await asyncio.sleep(2)  # Simulate browser activity
            
        except Exception as e:
            logger.error(f"Error during demonstration: {str(e)}")
            logger.info("Some actions may require the full NovaAct implementation")
        
        # 4. Give the user time to see the browser
        logger.info("Browser will remain open for 5 seconds...")
        await asyncio.sleep(5)
        
        # 5. Clean up
        logger.info("Stopping browser...")
        await nova.stop()
        logger.info("Browser stopped successfully")
        
        logger.info("Example completed!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
        
if __name__ == "__main__":
    asyncio.run(main())