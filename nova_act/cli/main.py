"""Main CLI module."""
import argparse
import asyncio
import sys

from nova_act import NovaAct, setup_logging

_LOGGER = setup_logging(__name__)

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(description="Nova ACT Framework CLI")
    return parser

def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        nova = NovaAct()
        asyncio.run(nova.start())
    except KeyboardInterrupt:
        _LOGGER.info("Shutting down...")
        sys.exit(0)
    except Exception as e:
        _LOGGER.error(f"Error: {e}")
        sys.exit(1)