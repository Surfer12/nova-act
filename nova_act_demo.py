#!/usr/bin/env python3
"""
Nova Act Demo Script
This script demonstrates basic usage of the Nova Act browser automation tool.
"""

from nova_act import NovaAct
import asyncio
import logging
import os
import tempfile

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set environment variables for debugging
os.environ["NOVA_ACT_LOG_LEVEL"] = str(logging.DEBUG)
os.environ["NOVA_ACT_BROWSER_ARGS"] = (
    "--start-maximized --no-sandbox --disable-gpu --window-size=1920,1080 --force-device-scale-factor=1 --disable-features=IsolateOrigins,site-per-process --disable-web-security --disable-site-isolation-trials"
)

# Create a temporary directory for user data
user_data_dir = os.path.join(tempfile.gettempdir(), "nova_act_user_data")
os.makedirs(user_data_dir, exist_ok=True)
logger.debug(f"Using user data directory: {user_data_dir}")


async def main() -> None:
    # Create a NovaAct instance
    nova = NovaAct(
        # Starting web page for the browser
        starting_page="https://www.google.com",
        # Set to False to see the browser in action
        headless=False,
        chrome_channel="chrome",  # Use Chrome
        screen_width=1920,  # Larger screen size
        screen_height=1080,
        user_data_dir=user_data_dir,  # Use specific user data directory
    )

    try:
        # Start the browser
        logger.debug("Starting Nova Act browser...")
        await nova.start()
        logger.debug("Browser started successfully")

        # Wait a moment for the browser to fully initialize
        await asyncio.sleep(2)

        # Perform a search action
        logger.debug("Performing search action...")
        result = await nova.act("Search for 'Nova Act browser automation'")
        logger.debug(f"Search result: {result}")

        # Print the result
        print(f"\nAction result: {result}")

        # Keep the browser open for a while
        input("\nPress Enter to close the browser...")

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        print(f"Error: {e}")

    finally:
        # Always stop the client to clean up resources
        logger.debug("Stopping Nova Act browser...")
        await nova.stop()
        logger.debug("Browser stopped successfully")
        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
