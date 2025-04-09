from pytest import mark, fixture  # Assuming pytest is used for async tests

from src.nova_act import ActResult, NovaAct
from src.nova_act.util.jsonschema import BOOL_SCHEMA


@mark.asyncio  # Decorator for async pytest functions
async def test_basic_functionality() -> None:
    """Test basic NovaAct functionality by performing a simple Google search."""
    # Create a NovaAct instance with the working configuration
    nova = NovaAct(
        starting_page="https://www.google.com",
        headless=False,
        chrome_channel="chromium",
        screen_width=1600,
        screen_height=900,
        user_data_dir=None,
    )

    try:
        # Start the browser
        await nova.start()

        # First verify we're on Google
        result: ActResult = await nova.act("Are we on google.com?", schema=BOOL_SCHEMA)
        assert result.matches_schema and result.parsed_response, (
            "Should be on Google.com"
        )

        # Try a simple search
        await nova.act("Search for 'Nova Act Amazon'")

        # Verify search results contain Amazon
        result = await nova.act(
            "Do the search results contain links to Amazon?",
            schema=BOOL_SCHEMA,
        )
        assert result.matches_schema and result.parsed_response, (
            "Search results should contain Amazon links"
        )

        print("Test completed successfully!")

    finally:
        # Always stop the client to clean up resources
        await nova.stop()


# Update main block if needed for async execution (or remove if using pytest runner)
# Example using asyncio.run if running standalone:
# import asyncio
# if __name__ == "__main__":
#     print("Running basic NovaAct test...")
#     asyncio.run(test_basic_functionality())

# If using pytest, the __main__ block might be unnecessary
# Keep the original if it serves another purpose, otherwise consider removing
if __name__ == "__main__":
    # This block might need adjustment depending on how async tests are run outside pytest
    print("Running basic NovaAct test (requires async runner like pytest-asyncio)...")
    # To run standalone: import asyncio; asyncio.run(test_basic_functionality())
    pass  # Placeholder, adjust or remove as needed
