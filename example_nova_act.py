#!/usr/bin/env python
# Import NovaAct from the package
from nova_act import NovaAct
from asyncio import run as asyncio_run


async def main() -> None:
    # Create a NovaAct instance
    nova = NovaAct(
        starting_page="https://www.google.com",
        # Set headless to False if you want to see the browser
        headless=False,
        chrome_channel="chromium",
        screen_width=1600,
        screen_height=900,
        user_data_dir=None,
    )

    try:
        # Start the client
        await nova.start()

        # Perform an action
        result = await nova.act("Search for 'Python programming language'")

        # Print the result
        print(f"Result: {result}")

        # Keep the browser open for a while
        input("\nPress Enter to close the browser...")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Make sure to stop the client to clean up resources
        await nova.stop()


if __name__ == "__main__":
    asyncio_run(main())
