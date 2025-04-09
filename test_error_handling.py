"""Tests for error handling in complex scenarios."""

import pytest
import asyncio
import json
from unittest.mock import patch, MagicMock, AsyncMock
from nova_act.nova_act import NovaAct
from nova_act.types.act_errors import (
    ActTimeoutError,
    ActExceededMaxStepsError,
    ActGuardrailsError,
    ActDispatchError,
    ActClientError,
    ActInternalServerError,
    ActServiceUnavailableError,
    ActRateLimitExceededError,
    ActProtocolError,
)


@pytest.fixture
def mock_metadata():
    """Create mock metadata for error testing."""
    from nova_act.types.act_metadata import ActMetadata

    return ActMetadata(
        start_time=123456789.0, end_time=123456790.0, elapsed_time=1.0, steps_taken=5
    )


@pytest.mark.asyncio
async def test_network_interruptions():
    """Test behavior when network is interrupted during operation."""
    with patch.object(
        NovaAct, "start", new_callable=AsyncMock
    ) as mock_start, patch.object(
        NovaAct, "stop", new_callable=AsyncMock
    ) as mock_stop, patch.object(
        NovaAct, "_send_message_to_browser", new_callable=AsyncMock
    ) as mock_send:
        # Simulate network interruption
        mock_send.side_effect = asyncio.TimeoutError("Network timeout")

        nova = NovaAct(headless=True)
        await nova.start()

        try:
            # Should raise a timeout error
            with pytest.raises(ActTimeoutError):
                await nova.act("What is the page title?")

        finally:
            await nova.stop()

        # Simulate connection reset
        mock_send.reset_mock()
        mock_send.side_effect = ConnectionResetError("Connection reset by peer")

        nova = NovaAct(headless=True)
        await nova.start()

        try:
            # Should raise a client error
            with pytest.raises(Exception):
                await nova.act("What is the page title?")

        finally:
            await nova.stop()


@pytest.mark.asyncio
async def test_browser_crash():
    """Test behavior when browser crashes during operation."""

    class MockBrowser:
        """Mock browser that crashes on certain operations."""

        def __init__(self):
            self.crashed = False

        async def send_message(self, message):
            """Mock send_message that crashes on second call."""
            if self.crashed:
                raise RuntimeError("Browser has crashed")
            if "trigger crash" in message.lower():
                self.crashed = True
                raise RuntimeError("Browser has crashed")
            return json.dumps({"result": "Success"})

    with patch.object(
        NovaAct, "start", new_callable=AsyncMock
    ) as mock_start, patch.object(
        NovaAct, "stop", new_callable=AsyncMock
    ) as mock_stop, patch.object(
        NovaAct, "_send_message_to_browser", new_callable=AsyncMock
    ) as mock_send:
        # Set up browser crash simulation
        mock_browser = MockBrowser()
        mock_send.side_effect = mock_browser.send_message

        nova = NovaAct(headless=True)
        await nova.start()

        try:
            # First request should succeed
            result = await nova.act("Simple request")
            assert "Success" in result.raw_response

            # Request that triggers crash should fail
            with pytest.raises(RuntimeError, match="Browser has crashed"):
                await nova.act("Trigger crash")

            # Subsequent requests should also fail
            with pytest.raises(RuntimeError, match="Browser has crashed"):
                await nova.act("Another request")

        finally:
            await nova.stop()


@pytest.mark.asyncio
async def test_server_errors():
    """Test behavior with various server errors."""
    with patch.object(
        NovaAct, "start", new_callable=AsyncMock
    ) as mock_start, patch.object(
        NovaAct, "stop", new_callable=AsyncMock
    ) as mock_stop, patch.object(
        NovaAct, "_send_message_to_browser", new_callable=AsyncMock
    ) as mock_send:
        # Set up a response for each type of server error
        server_error_responses = [
            {"status": "error", "code": 500, "message": "Internal Server Error"},
            {"status": "error", "code": 503, "message": "Service Unavailable"},
            {"status": "error", "code": 429, "message": "Rate Limit Exceeded"},
        ]

        for error_response in server_error_responses:
            mock_send.reset_mock()
            mock_send.return_value = json.dumps(error_response)

            nova = NovaAct(headless=True)
            await nova.start()

            try:
                # Should raise appropriate error types
                with pytest.raises(Exception) as exc_info:
                    await nova.act("What is the page title?")

                # Check if exception contains expected error message
                error_message = error_response["message"]
                assert error_message.lower() in str(exc_info.value).lower()

            finally:
                await nova.stop()


@pytest.mark.asyncio
async def test_multiple_act_calls():
    """Test behavior with multiple sequential act calls."""
    nova = NovaAct(headless=True)
    await nova.start()

    try:
        # Make multiple sequential calls
        results = []
        for i in range(3):
            result = await nova.act(f"What is {i}+{i}?")
            results.append(result)

        # All calls should return results
        assert len(results) == 3
        assert all(hasattr(r, "raw_response") for r in results)

        # Try making concurrent calls
        tasks = [
            nova.act("What is 1+1?"),
            nova.act("What is 2+2?"),
            nova.act("What is 3+3?"),
        ]

        # This might raise exceptions depending on whether the implementation
        # supports concurrent calls, so we gather with return_exceptions=True
        concurrent_results = await asyncio.gather(*tasks, return_exceptions=True)

        # At least some of the results should be either ActResults or Exceptions
        assert len(concurrent_results) == 3
        assert all(
            hasattr(r, "raw_response") or isinstance(r, Exception)
            for r in concurrent_results
        )

    finally:
        await nova.stop()


@pytest.mark.asyncio
async def test_recovery_from_errors():
    """Test recovery from errors in subsequent act calls."""
    with patch.object(
        NovaAct, "start", new_callable=AsyncMock
    ) as mock_start, patch.object(
        NovaAct, "stop", new_callable=AsyncMock
    ) as mock_stop, patch.object(
        NovaAct, "_send_message_to_browser", new_callable=AsyncMock
    ) as mock_send:
        # Set up to fail on first call, succeed on second
        call_count = 0

        async def mock_send_message(message):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call fails
                raise RuntimeError("Simulated error")
            else:
                # Subsequent calls succeed
                return json.dumps(
                    {"result": f"Success on call {call_count}", "status": "success"}
                )

        mock_send.side_effect = mock_send_message

        nova = NovaAct(headless=True)
        await nova.start()

        try:
            # First call should fail
            with pytest.raises(RuntimeError):
                await nova.act("First request")

            # Second call should succeed
            result = await nova.act("Second request")
            assert "Success on call 2" in result.raw_response

        finally:
            await nova.stop()


@pytest.mark.asyncio
async def test_malformed_schemas():
    """Test act with invalid schemas."""
    nova = NovaAct(headless=True)
    await nova.start()

    try:
        # Test with syntactically invalid schema
        with pytest.raises(Exception):
            await nova.act(
                "What is the page title?", schema="This is not a valid JSON schema"
            )

        # Test with invalid schema type
        with pytest.raises(Exception):
            await nova.act("What is the page title?", schema={"type": "invalid_type"})

        # Test with schema that's missing required fields
        with pytest.raises(Exception):
            await nova.act(
                "What is the page title?",
                schema={"required": ["field_that_doesnt_exist"]},
            )

    finally:
        await nova.stop()
