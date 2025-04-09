import asyncio
import argparse
import json
import logging
import sys
from pathlib import Path

# Set up argument parser
parser = argparse.ArgumentParser(description="Nova ACT Server")
parser.add_argument("--config", help="Path to configuration file", default="configs/dev.json")
parser.add_argument("--debug", help="Enable debug mode", action="store_true")
parser.add_argument("--log-level", help="Logging level", default="info")
parser.add_argument("--optimize", help="Enable optimization", action="store_true")
parser.add_argument("--test-mode", help="Run in test mode", action="store_true")
args = parser.parse_args()

# Set up logging first
log_level = getattr(logging, args.log_level.upper(), logging.INFO)
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Add the src directory to Python path first to ensure we use the correct implementation
src_path = str(Path(__file__).parent / "src")
logger.info(f"Adding to Python path: {src_path}")
sys.path.insert(0, src_path)  # Use insert(0, ...) to ensure src path has priority

# Import from the full implementation
try:
    from nova_act.bridge import NovaActBridge
    logger.info("Using full NovaActBridge implementation")
except (ImportError, TypeError) as e:
    logger.error(f"Error importing full NovaActBridge: {e}")
    sys.exit(1)

# Load configuration if provided
try:
    with open(args.config, "r") as f:
        config = json.load(f)
        logger.info(f"Loaded configuration from {args.config}")
        
        if args.debug:
            logger.info("Debug mode enabled")
        if args.optimize:
            logger.info("Optimization enabled")
        if args.test_mode:
            logger.info("Test mode enabled")
            
        logger.debug(f"Configuration: {json.dumps(config, indent=2)}")
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.warning(f"Failed to load configuration from {args.config}: {e}")
    logger.info("Using default configuration")
    config = {"environment": "development"}


async def main():
    """Start the Nova Act WebSocket server."""
    # Get host and port from config or use defaults
    host = config.get("api", {}).get("host", "localhost")
    port = config.get("api", {}).get("port", 8081)
    
    bridge = NovaActBridge(host=host, port=port)
    try:
        logger.info(f"Starting Nova Act WebSocket server on {host}:{port}...")
        await bridge.start()
        logger.info(f"Server running on ws://{host}:{port}")

        # Keep the server running
        await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await bridge.stop()
    except Exception as e:
        logger.error(f"Error running server: {e}")
        try:
            await bridge.stop()
        except Exception as stop_error:
            logger.error(f"Error stopping server: {stop_error}")


if __name__ == "__main__":
    asyncio.run(main())
