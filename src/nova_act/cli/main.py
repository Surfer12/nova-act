"""Main module for Nova ACT."""

import argparse
import json
import logging
import sys
from typing import Dict, TypedDict


class NovaActConfig(TypedDict, total=False):
    """Type definition for Nova ACT configuration."""

    environment: str
    logging: Dict[str, str]
    browser: Dict[str, object]


def load_config(config_file: str) -> NovaActConfig:
    """Load configuration from a JSON file."""
    with open(config_file, "r") as f:
        config_data = json.load(f)
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


def setup_logging(log_level: str = "info") -> None:
    """Configure logging based on the specified log level."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def async_main() -> None:
    """Run the Nova ACT application asynchronously."""
    parser = argparse.ArgumentParser(description="Nova ACT")
    parser.add_argument("--config", help="Path to configuration file", required=True)
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    parser.add_argument("--log-level", help="Logging level", default="info")
    parser.add_argument("--optimize", help="Enable optimization", action="store_true")
    parser.add_argument("--test-mode", help="Run in test mode", action="store_true")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

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
            import asyncio

            # Get browser config from config.json
            browser_config = config.get("browser", {})
            starting_page = browser_config.get("starting_page", "https://www.google.com")
            headless = browser_config.get("headless", True)

            logger.info(f"Launching browser with starting page: {starting_page}")

            # Initialize and start NovaAct
            nova = NovaAct(
                starting_page=starting_page,
                headless=headless,
            )

            # Start the browser (this will open it) - properly awaiting the async function
            await nova.start()

            # Keep the browser open until user interrupts
            logger.info("Browser launched. Press Ctrl+C to exit.")
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("User interrupted. Closing browser...")
            finally:
                # Clean up - properly awaiting the async function
                await nova.stop()

        except ImportError as e:
            logger.error(f"Failed to import NovaAct: {e}")
            logger.info("Running in minimal mode without browser...")

            # Just sleep to keep the process alive for demo purposes
            import time
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("User interrupted. Exiting...")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def main() -> None:
    """Run the Nova ACT application by calling the async main function."""
    import asyncio
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
