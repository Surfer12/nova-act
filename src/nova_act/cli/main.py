"""Main module for Nova ACT."""

import argparse
import json
import logging
import sys
from typing import Dict, TypedDict


class NovaActConfig(TypedDict):
    """Type definition for Nova ACT configuration."""

    environment: str
    logging: Dict[str, str]


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
            logging={str(k): str(v) for k, v in config_data["logging"].items()}
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


def main() -> None:
    """Run the Nova ACT application."""
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
        _ = load_config(args.config)  # Config loaded but not used in this part of the code

        logger.info(f"Starting Nova ACT with configuration from {args.config}")
        if args.debug:
            logger.debug("Debug mode enabled")
        if args.optimize:
            logger.info("Optimization enabled")
        if args.test_mode:
            logger.info("Running in test mode")

        # Here you would add your actual application logic

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
