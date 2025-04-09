import asyncio
import logging
import os
from nova_act import NovaAct

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Test basic Nova Act functionality."""
    logger.info("Testing basic Nova Act functionality...")
    try:
        # Revised: Initialize Nova Act using a configuration dictionary for clarity
        logger.debug("Initializing Nova Act using revised configuration...")
        config = {
            "browser_url": "https://www.google.com",
            "headless": False,
            "chrome_channel": "chromium",  # Use Chromium specifically
            "screen_width": 1600,
            "screen_height": 900,
            "user_data_dir": None,  # Use a fresh profile
        }
        nova = NovaAct(**config)

        # Start the client
        logger.debug("Starting Nova Act client...")
        await nova.start()
        logger.info("Nova Act started successfully!")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        # Print environment variables (without sensitive data)
        logger.debug(f"Environment variables: {dict(os.environ)}")
    finally:
        # Make sure to stop the client
        if "nova" in locals():
            logger.debug("Stopping Nova Act client...")
            await nova.stop()
            logger.info("Nova Act stopped.")


if __name__ == "__main__":
    asyncio.run(main())
