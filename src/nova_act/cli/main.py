"""Main module for Nova ACT."""

import argparse
import json
import logging
import sys
import time
import traceback
from asyncio import get_running_loop
from json import dumps, loads
from typing import Dict, TypedDict

from nova_act.util.logging import setup_logging


class NovaActConfig(TypedDict, total=False):
    """Type definition for Nova ACT configuration."""

    environment: str
    logging: Dict[str, str]
    browser: Dict[str, object]


def load_config(config_file: str) -> NovaActConfig:
    """Load configuration from a JSON file."""
    with open(config_file, "r") as f:
        config_data = loads(f.read())
        # Validate the required fields
        if not isinstance(config_data, dict):
            raise ValueError("Config must be a JSON object")
        if "environment" not in config_data:
            raise ValueError("Config must contain 'environment' field")
        if "logging" not in config_data:
            raise ValueError("Config must contain 'logging' field")
        if not isinstance(config_data["logging"], dict):
            raise ValueError("Config 'logging' field must be an object")
        return NovaActConfig(
            environment=str(config_data["environment"]),
            logging={str(k): str(v) for k, v in config_data["logging"].items()},
        )


def main() -> None:
    """Run the Nova ACT application."""
    # Detect if we're running inside an asyncio event loop already
    try:
        from asyncio import run as async_run

        try:
            loop = get_running_loop()
            running_in_asyncio = True
        except RuntimeError:
            running_in_asyncio = False
    except ImportError:
        running_in_asyncio = False

    # If we're already in an asyncio loop, we can't use the sync Playwright API
    if running_in_asyncio:
        print("Error: nova-act.sh cannot be run inside an asyncio loop.")
        print("Please use nova-act-sync.sh instead, which runs without asyncio.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Nova ACT")
    parser.add_argument("--config", help="Path to configuration file", required=True)
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    parser.add_argument("--log-level", help="Logging level", default="info")
    parser.add_argument("--optimize", help="Enable optimization", action="store_true")
    parser.add_argument("--test-mode", help="Run in test mode", action="store_true")

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging(__name__, args.log_level)

    try:
        # Load configuration
        config = load_config(args.config)

        logger.info(f"Starting Nova ACT with configuration from {args.config}")
        if args.debug:
            logger.debug("Debug mode enabled")
        if args.optimize:
            logger.info("Optimization enabled")
        if args.test_mode:
            logger.info("Running in test mode")

        # Import here to avoid circular imports
        try:
            from nova_act import NovaAct
            import time

            # Get browser config from config.json
            browser_config = config.get("browser", {})
            starting_page = browser_config.get(
                "starting_page", "https://www.google.com"
            )
            headless = browser_config.get("headless", True)

            logger.info(f"Launching browser with starting page: {starting_page}")

            # Initialize NovaAct
            nova = NovaAct(
                starting_page=starting_page,
                headless=headless,
            )

            # Start the browser directly (this is synchronous)
            nova.start()

            # Keep the browser open until user interrupts
            logger.info("Browser launched. Press Ctrl+C to exit.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("User interrupted. Closing browser...")
            finally:
                # Clean up
                nova.stop()

        except ImportError as e:
            logger.error(f"Failed to import NovaAct: {e}")
            logger.info("Running in minimal mode without browser...")

            # Just sleep to keep the process alive for demo purposes
            try:
                while True:
                    import time

                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("User interrupted. Exiting...")

    except Exception as e:
        import traceback

        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


# Previous async main function and run removed


if __name__ == "__main__":
    main()
