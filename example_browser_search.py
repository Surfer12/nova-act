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

                logger.warning(
                    "Using core NovaAct implementation (minimal functionality)"
                )

        # 1. Create NovaAct instance with Chromium if possible
        logger.info("Creating NovaAct instance...")

        # Try different combinations of parameters to find what works
        try:
            # First try with all parameters
            nova = NovaAct(
                headless=False,  # Use visible browser for demonstration
                chrome_channel="chromium",  # Specifically use Chromium browser
            )
        except TypeError as e:
            if "chrome_channel" in str(e):
                logger.warning(
                    "Implementation doesn't support chrome_channel, trying without it"
                )
                try:
                    # Try with just headless
                    nova = NovaAct(headless=False)
                except TypeError:
                    logger.warning(
                        "Implementation doesn't support headless, using default parameters"
                    )
                    # Last resort: no parameters
                    nova = NovaAct()
            elif "headless" in str(e):
                logger.warning(
                    "Implementation doesn't support headless, trying just chrome_channel"
                )
                try:
                    # Try with just chrome_channel
                    nova = NovaAct(chrome_channel="chromium")
                except TypeError:
                    logger.warning(
                        "Implementation supports neither headless nor chrome_channel, using default"
                    )
                    # Last resort: no parameters
                    nova = NovaAct()
            else:
                # Something else went wrong
                logger.warning(
                    f"Error initializing NovaAct: {e}, using default parameters"
                )
                nova = NovaAct()

        logger.info("NovaAct instance created successfully")

        # 2. Start the browser (if supported)
        logger.info("Starting browser...")
        try:
            # Check which method exists: start() or connect()
            if hasattr(nova, "start") and callable(getattr(nova, "start")):
                await nova.start()
                logger.info("Browser started with nova.start()")
            elif hasattr(nova, "connect") and callable(getattr(nova, "connect")):
                # connect() method is available in some implementations
                await nova.connect()
                logger.info("Browser started with nova.connect()")
            else:
                logger.warning(
                    "No start/connect method found, browser may not have started properly"
                )
        except Exception as e:
            logger.error(f"Error starting browser: {str(e)}")
            logger.warning("Continuing with example despite browser start failure")

        # 3. Demonstrate basic browser actions
        logger.info("Demonstrating browser actions...")

        # This will vary based on which implementation is available
        try:
            # Check what methods are available for browser actions
            has_act_method = hasattr(nova, "act") and callable(getattr(nova, "act"))
            has_bridge = hasattr(nova, "bridge") and nova.bridge is not None
            is_connected = hasattr(nova, "connected") and nova.connected

            if has_act_method:
                # Using implementation with act() method for natural language instructions
                logger.info("Using implementation with act() method")

                # Navigate to Google
                logger.info("Navigating to Google...")
                await nova.act("go to google.com")

                # Perform a search
                logger.info("Performing search for 'Nova Act browser automation'...")
                await nova.act("search for Nova Act browser automation")

                # Wait for search results and click first result
                logger.info("Clicking on first search result...")
                await nova.act("click on the first search result")

                # Wait a moment to see the result
                await asyncio.sleep(3)
            elif has_bridge and is_connected:
                # Using bridge API
                logger.info("Using bridge API")
                logger.info("Would use bridge API to control browser")
                logger.info("Bridge connected: " + str(is_connected))
                await asyncio.sleep(1)
            else:
                # Using minimal implementation or alternative API
                logger.info(
                    "Implementation doesn't support act() method or bridge isn't available"
                )
                logger.info("Simulating browser actions")
                await asyncio.sleep(2)  # Simulate browser activity

        except Exception as e:
            logger.error(f"Error during demonstration: {str(e)}")
            logger.info("Some actions may require the full NovaAct implementation")

        # 4. Give the user time to see the browser
        logger.info("Browser will remain open for 5 seconds...")
        await asyncio.sleep(5)

        # 5. Clean up
        logger.info("Stopping browser...")
        try:
            # Check which method exists: stop() or disconnect()
            if hasattr(nova, "stop") and callable(getattr(nova, "stop")):
                await nova.stop()
                logger.info("Browser stopped with nova.stop()")
            elif hasattr(nova, "disconnect") and callable(getattr(nova, "disconnect")):
                # disconnect() method is available in some implementations
                await nova.disconnect()
                logger.info("Browser stopped with nova.disconnect()")
            else:
                logger.warning(
                    "No stop/disconnect method found, browser may not have stopped properly"
                )
        except Exception as e:
            logger.error(f"Error stopping browser: {str(e)}")
            logger.warning("Example completed but browser may still be running")

        logger.info("Example completed!")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
