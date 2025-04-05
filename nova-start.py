import logging
import os

from nova_act import NovaAct

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main() -> None:
    """Test basic Nova Act functionality."""
    logger.info("Testing basic Nova Act functionality...")

    try:
        # Initialize Nova Act with specific configuration
        logger.debug("Initializing Nova Act...")
        nova = NovaAct(
            starting_page="https://www.google.com",
            headless=False,
            chrome_channel="chromium",  # Use Chromium specifically
            screen_width=1600,
            screen_height=900,
            user_data_dir=None,  # Use a fresh profile
        )

        # Start the client
        logger.debug("Starting Nova Act client...")
        nova.start()
        logger.info("Nova Act started successfully!")

        # Try a simple search
        logger.info("\nPerforming a simple search...")
        nova.act("search for Nova Act Amazon")
        logger.info("Search completed!")

        # Keep the browser open for a while
        input("\nPress Enter to close the browser...")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        # Print environment variables (without sensitive data)
        logger.debug(f"Environment variables: {dict(os.environ)}")
    finally:
        # Make sure to stop the client
        if "nova" in locals():
            logger.debug("Stopping Nova Act client...")
            nova.stop()
            logger.info("Nova Act stopped.")


if __name__ == "__main__":
    main()
