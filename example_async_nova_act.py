#!/usr/bin/env python3
"""
Example script demonstrating how to use Nova Act's async API.
This script properly handles the asynchronous nature of Nova Act.
"""

import asyncio
import argparse
import sys


async def main():
    """Run an asynchronous Nova Act session."""
    # Import inside the function to avoid import errors when NovaAct is not available
    try:
        from nova_act import NovaAct
    except ImportError:
        print("Error: Nova Act is not installed or not available in the Python path.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Example of using Nova Act's async API"
    )
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--url", default="https://www.google.com", help="Starting URL")
    args = parser.parse_args()

    # Create a Nova Act instance with the async bridge enabled
    nova = NovaAct(
        starting_page=args.url,
        headless=args.headless,
        enable_bridge=True,  # Enable the WebSocket bridge for real-time updates
    )

    try:
        # Start the browser asynchronously (this also starts the WebSocket bridge)
        print(f"Starting Nova Act browser at {args.url}...")
        await nova.start_async()
        print("Browser started!")

        # Example: Execute a search
        print("Performing a Google search for 'Nova Act browser automation'...")
        result = await nova.act("search for Nova Act browser automation")
        print(f"Search completed with result: {result.success}")

        # Keep the browser open for demo purposes
        print("\nBrowser will remain open for 30 seconds. Press Ctrl+C to exit early.")
        for i in range(30, 0, -1):
            print(f"\rClosing in {i} seconds...", end="")
            await asyncio.sleep(1)
        print("\rClosing now!            ")

    except KeyboardInterrupt:
        print("\nUser interrupted. Closing browser...")
    except Exception as e:
        print(f"\nError during Nova Act execution: {e}")
    finally:
        # Always ensure we stop the browser and WebSocket bridge properly
        if nova:
            print("Stopping Nova Act browser...")
            await nova.stop_async()
            print("Browser stopped!")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
