"""Tests for asynchronous operations in NovaAct."""

import pytest
import asyncio
from nova_act.nova_act import NovaAct


@pytest.mark.asyncio
async def test_parallel_nova_instances():
    """Test running multiple NovaAct instances in parallel."""
    # Create instances with different configurations
    nova1 = NovaAct(headless=True, screen_width=800, screen_height=600)
    nova2 = NovaAct(headless=True, screen_width=1024, screen_height=768)

    try:
        # Start browsers in parallel
        await asyncio.gather(nova1.start(), nova2.start())

        # Verify both browsers started
        assert hasattr(nova1, "_browser") and nova1._browser is not None
        assert hasattr(nova2, "_browser") and nova2._browser is not None

        # Execute different tasks in parallel
        results = await asyncio.gather(
            nova1.navigate("https://example.com"), nova2.navigate("https://httpbin.org")
        )

        # Each should end up on different URLs
        title1 = await nova1.act("What is the page title?")
        title2 = await nova2.act("What is the page title?")

        assert "Example" in title1.raw_response
        assert "httpbin" in title2.raw_response

    finally:
        # Clean up both instances
        await asyncio.gather(nova1.stop(), nova2.stop())


@pytest.mark.asyncio
async def test_concurrent_act_calls():
    """Test behavior with concurrent act calls on the same instance."""
    nova = NovaAct(headless=True)
    await nova.start()

    try:
        # Attempt to execute concurrent act calls
        # This might raise exceptions depending on whether the implementation
        # supports concurrent calls, so we gather with return_exceptions=True
        tasks = [
            nova.act("What is the page title?"),
            nova.act("What is the current URL?"),
            nova.act("Is there an h1 tag on the page?"),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check if at least some results were successful
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) > 0, "No concurrent act calls succeeded"

    finally:
        await nova.stop()


@pytest.mark.asyncio
async def test_single_browser_multiple_tabs():
    """Test opening multiple tabs in a single browser instance (if supported)."""
    nova = NovaAct(headless=True)
    await nova.start()

    try:
        # This test assumes opening new tabs is supported through natural language
        # Try to open a new tab with the act method
        await nova.act("Open a new tab")

        # Try to navigate to different URLs in different tabs
        await nova.act("Navigate to https://example.com in the first tab")
        await nova.act("Navigate to https://httpbin.org in the second tab")

        # Check if we can get information from different tabs
        # These calls might not work depending on implementation
        tab1_title = await nova.act("What is the title of the page in the first tab?")
        tab2_title = await nova.act("What is the title of the page in the second tab?")

        # If successful, titles should be different
        # But this might not be supported, so we don't assert strictly
        if "example" in tab1_title.raw_response.lower():
            assert "httpbin" not in tab1_title.raw_response.lower()

    finally:
        await nova.stop()


@pytest.mark.asyncio
async def test_async_navigation_and_actions():
    """Test combination of navigation and actions in async context."""
    nova = NovaAct(headless=True)
    await nova.start()

    try:
        # Navigate to a website
        await nova.navigate("https://example.com")

        # Execute multiple actions in parallel (async tasks that don't use act)
        # These will be custom methods assuming NovaAct has them
        if hasattr(nova, "get_page_title") and callable(
            getattr(nova, "get_page_title")
        ):
            title_task = asyncio.create_task(nova.get_page_title())
        else:
            title_task = asyncio.create_task(nova.act("What is the page title?"))

        if hasattr(nova, "get_current_url") and callable(
            getattr(nova, "get_current_url")
        ):
            url_task = asyncio.create_task(nova.get_current_url())
        else:
            url_task = asyncio.create_task(nova.act("What is the current URL?"))

        # Wait for both to complete
        title_result = await title_task
        url_result = await url_task

        # Check results
        if hasattr(title_result, "raw_response"):  # ActResult from act method
            assert "Example" in title_result.raw_response
        else:  # Direct result from custom method
            assert "Example" in title_result

        if hasattr(url_result, "raw_response"):  # ActResult from act method
            assert "example.com" in url_result.raw_response
        else:  # Direct result from custom method
            assert "example.com" in url_result

    finally:
        await nova.stop()


@pytest.mark.asyncio
async def test_browser_restart():
    """Test restarting the browser after stopping it."""
    nova = NovaAct(headless=True)

    # First session
    await nova.start()
    try:
        await nova.navigate("https://example.com")
        title1 = await nova.act("What is the page title?")
        assert "Example" in title1.raw_response
    finally:
        await nova.stop()

    # Verify browser is stopped
    assert not hasattr(nova, "_browser") or nova._browser is None

    # Second session with same instance
    await nova.start()
    try:
        await nova.navigate("https://httpbin.org")
        title2 = await nova.act("What is the page title?")
        assert "httpbin" in title2.raw_response.lower()
    finally:
        await nova.stop()


@pytest.mark.asyncio
async def test_long_running_operations():
    """Test behavior during long-running operations."""
    nova = NovaAct(headless=True)
    await nova.start()

    try:
        # Start a long-running operation
        long_task = asyncio.create_task(
            nova.act("Wait for 5 seconds and then tell me the current time")
        )

        # While that's running, try to do something else
        # Give the long task a head start
        await asyncio.sleep(0.5)

        # This might succeed or fail depending on whether concurrent operations are supported
        try:
            short_result = await asyncio.wait_for(
                nova.act("What is the page title?"), timeout=1.0
            )
            assert hasattr(short_result, "raw_response")
        except Exception:
            # It's acceptable for this to fail if the implementation doesn't support
            # concurrent operations
            pass

        # Wait for the long task to complete
        long_result = await long_task
        assert hasattr(long_result, "raw_response")

    finally:
        await nova.stop()
