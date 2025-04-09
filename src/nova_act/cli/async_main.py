"""Asynchronous main module for Nova ACT."""

import argparse
import asyncio
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
    parser = argparse.ArgumentParser(description="Nova ACT (Async)")
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

        logger.info(f"Starting Nova ACT (Async) with configuration from {args.config}")
        if args.debug:
            logger.debug("Debug mode enabled")
        if args.optimize:
            logger.info("Optimization enabled")
        if args.test_mode:
            logger.info("Running in test mode")

        # Import here to avoid circular imports
        try:
            from nova_act import NovaAct

            # Get browser config from config.json
            browser_config = config.get("browser", {})
            starting_page = browser_config.get(
                "starting_page", "https://www.google.com"
            )
            headless = browser_config.get("headless", True)

            logger.info(f"Launching browser with starting page: {starting_page}")

            # Initialize NovaAct with bridge enabled
            nova = NovaAct(
                starting_page=starting_page,
                headless=headless,
                enable_bridge=True,  # Enable bridge for async operation
            )

            # Start the browser asynchronously
            await nova.start_async()

            logger.info("Browser launched asynchronously. Press Ctrl+C to exit.")

            # Keep running until interrupted
            try:
                # This will run forever until interrupted
                while True:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                logger.info("Task was cancelled. Closing browser...")
            except KeyboardInterrupt:
                logger.info("User interrupted. Closing browser...")
            finally:
                # Clean up
                await nova.stop_async()

        except ImportError as e:
            logger.error(f"Failed to import NovaAct: {e}")
            logger.info("Running in minimal mode without browser...")

            # Just sleep to keep the process alive for demo purposes
            try:
                while True:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                pass
            except KeyboardInterrupt:
                logger.info("User interrupted. Exiting...")

    except Exception as e:
        import traceback

        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


def main() -> None:
    """Entry point for the async CLI."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt...")


if __name__ == "__main__":
    main()
