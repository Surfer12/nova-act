"""Tests for verifying architectural components and their interactions."""

from asyncio import run as async_run
from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from nova_act.bridge.client import BridgeClient
from nova_act.types.act_result import ActResult
from nova_act.nova_act import NovaAct
from nova_act.util.logging import setup_logging
from nova_act import __version__


class TestArchitecture(unittest.TestCase):
    """Test cases for verifying architectural components."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_url = "https://example.com"
        self.test_prompt = "test prompt"

    @patch("nova_act.bridge.BridgeClient", autospec=True)
    def test_nova_act_bridge_interaction(self, mock_bridge: MagicMock) -> None:
        """Test interaction between NovaAct and Bridge layer."""
        # Setup mock
        mock_bridge.return_value = AsyncMock()

        # Create NovaAct instance
        nova = NovaAct()

        # Verify bridge client was created with correct parameters
        # BridgeClient is created during start()
        self.assertIsNone(nova._bridge_client)

        # Start the NovaAct instance
        loop = asyncio.get_event_loop()
        loop.run_until_complete(nova.start())

        mock_bridge.assert_called_once()
        self.assertIsNotNone(nova._bridge_client)

    def test_act_result_schema_validation(self) -> None:
        """Test ActResult schema validation functionality."""
        # Create test data
        success_result = ActResult(
            success=True, message="Test success", data={"test": "value"}
        )
        self.assertTrue(success_result)

        error_result = ActResult(
            success=False, message="Test error", error=Exception("Test exception")
        )
        self.assertFalse(error_result)


if __name__ == "__main__":
    unittest.main()
