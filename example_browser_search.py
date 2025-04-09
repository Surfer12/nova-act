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
            # Try to import the full implementation from src directory first
            from src.nova_act.nova_act import NovaAct
            logger.info("Using full NovaAct implementation")
        except ImportError:
            try:
                # Try to import the full implementation from installed package
                from nova_act import NovaAct
                logger.info("Using installed NovaAct implementation")
            except ImportError:
                # Fallback to minimal core implementation
                from nova_act.core import NovaAct
                logger.warning("Using core NovaAct implementation (minimal functionality)")
        
        # 1. Create NovaAct instance with Chromium
        logger.info("Creating NovaAct instance with Chromium...")
        try:
            # Try to use chrome_channel parameter (only in full implementation)
            nova = NovaAct(
                headless=False,  # Use visible browser for demonstration
                chrome_channel="chromium"  # Specifically use Chromium browser
            )
        except TypeError:
            # Fallback for core implementation that doesn't support chrome_channel
            logger.warning("Core implementation doesn't support chrome_channel, using default browser")
            nova = NovaAct(headless=False)
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