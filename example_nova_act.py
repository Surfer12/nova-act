#!/usr/bin/env python
# Import NovaAct from the package
from nova_act import NovaAct
import os
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main():
    """Main async function to handle NovaAct operations"""
    try:
        # Check for API key
        api_key = os.getenv("NOVA_ACT_API_KEY")
        if not api_key:
            raise ValueError(
                "NOVA_ACT_API_KEY environment variable is not set. Please set it in your .env file."
            )
        logger.debug(f"Using API key: {api_key[:4]}...{api_key[-4:]}")

        # Print environment variables for debugging
        logger.debug("Environment variables:")
        for key, value in os.environ.items():
            if key.startswith("NOVA_ACT_"):
                logger.debug(f"{key}: {value}")

        # Create a NovaAct instance
        nova = NovaAct(
            starting_page="https://www.google.com",
            headless=True,
            chrome_channel="chromium",
            screen_width=1600,
            screen_height=900,
            user_data_dir=None,
        )
        logger.debug("NovaAct instance created successfully")

        try:
            # Start the client (sync operation)
            logger.debug("Starting NovaAct client...")
            nova.start()  # This is a sync operation
            logger.debug("NovaAct client started successfully")

            # Perform an action (async operation)
            logger.debug("Performing action...")
            result = await nova.act(
                "Search for 'Python programming language'"
            )  # This is an async operation
            logger.debug(f"Action completed with result: {result}")
            print(f"Result: {result}")

        finally:
            # Make sure to stop the client to clean up resources (sync operation)
            if nova.started:
                logger.debug("Stopping NovaAct client...")
                nova.stop()  # This is a sync operation
                logger.debug("NovaAct client stopped successfully")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}", exc_info=True)
        raise
