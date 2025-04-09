"""Tests for NovaAct browser interactions."""

from pytest import mark, fixture
from nova_act.nova_act import NovaAct


@mark.asyncio
async def test_browser_navigation():
    """Test basic browser navigation."""
    nova = NovaAct()
    await nova.start()
    try:
        # Test navigation
        await nova.navigate("https://example.com")
        # Add navigation assertions
    finally:
        await nova.stop()


@mark.asyncio
async def test_browser_interaction():
    """Test browser interaction capabilities."""
    nova = NovaAct(headless=True)
    await nova.start()
    try:
        await nova.navigate("https://example.com")

        # Test page title
        page_title = await nova.act("What is the page title?")
        assert "Example Domain" in page_title.raw_response

        # Test page content
        content_check = await nova.act(
            "Is there text that says 'Example Domain' on the page?",
            schema={"type": "boolean"},
        )
        assert content_check.matches_schema
        assert content_check.parsed_response is True

    finally:
        await nova.stop()


@mark.asyncio
async def test_error_handling():
    """Test error handling in browser operations."""
    nova = NovaAct()
    with pytest.raises(Exception):
        # Test invalid operations
        await nova.navigate("invalid-url")
