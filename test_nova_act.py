from nova_act import NovaAct, BOOL_SCHEMA


def test_basic_functionality():
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
        nova.start()

        # First verify we're on Google
        result = nova.act("Are we on google.com?", schema=BOOL_SCHEMA)
        assert result.matches_schema and result.parsed_response, (
            "Should be on Google.com"
        )

        # Try a simple search
        nova.act("Search for 'Nova Act Amazon'")

        # Verify search results contain Amazon
        result = nova.act(
            "Do the search results contain links to Amazon?", schema=BOOL_SCHEMA
        )
        assert result.matches_schema and result.parsed_response, (
            "Search results should contain Amazon links"
        )

        print("Test completed successfully!")

    finally:
        # Always stop the client to clean up resources
        nova.stop()


if __name__ == "__main__":
    print("Running basic NovaAct test...")
    test_basic_functionality()
