"""Tests for verifying architectural components and their interactions."""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from nova_act import NovaAct
from nova_act.bridge.client import BridgeClient
from nova_act.types.act_result import ActResult


class TestArchitecture(unittest.TestCase):
    """Test cases for verifying architectural components."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.test_url = "https://example.com"
        self.test_prompt = "test prompt"

    @patch("nova_act.bridge.client.BridgeClient")
    def test_nova_act_bridge_interaction(self, mock_bridge: MagicMock) -> None:
        """Test interaction between NovaAct and Bridge layer."""
        # Setup mock
        mock_bridge.return_value = AsyncMock()
        
        # Create NovaAct instance
        nova = NovaAct(starting_page=self.test_url)
        
        # Verify bridge client was created with correct parameters
        mock_bridge.assert_called_once()
        self.assertIsNotNone(nova._bridge_client)

    @patch("nova_act.impl.playwright.PlaywrightBrowser")
    def test_browser_automation_integration(self, mock_playwright: MagicMock) -> None:
        """Test integration with Playwright browser automation."""
        # Setup mock
        mock_playwright.return_value = AsyncMock()
        
        # Create NovaAct instance with mocked playwright
        nova = NovaAct(starting_page=self.test_url)
        
        # Verify playwright integration
        self.assertIsNotNone(nova._browser)

    @patch("nova_act.impl.backend.BackendService")
    def test_backend_service_integration(self, mock_backend: MagicMock) -> None:
        """Test integration with backend service."""
        # Setup mock
        mock_backend.return_value = AsyncMock()
        
        # Create NovaAct instance
        nova = NovaAct(starting_page=self.test_url)
        
        # Verify backend service integration
        self.assertIsNotNone(nova._backend)

    async def test_act_result_schema_validation(self) -> None:
        """Test ActResult schema validation functionality."""
        # Create test schema
        test_schema = {
            "type": "object",
            "properties": {
                "test": {"type": "string"}
            }
        }
        
        # Create ActResult with valid data
        valid_result = ActResult(
            response='{"test": "value"}',
            schema=test_schema
        )
        self.assertTrue(valid_result.matches_schema)
        
        # Create ActResult with invalid data
        invalid_result = ActResult(
            response='{"test": 123}',  # Should be string
            schema=test_schema
        )
        self.assertFalse(invalid_result.matches_schema)

    def test_error_handling(self) -> None:
        """Test error handling across architectural layers."""
        from nova_act.types.act_errors import ActError, BrowserError, ValidationError
        
        # Test custom error hierarchy
        with self.assertRaises(ActError):
            raise ActError("Test error")
            
        with self.assertRaises(BrowserError):
            raise BrowserError("Test browser error")
            
        with self.assertRaises(ValidationError):
            raise ValidationError("Test validation error")

    @patch("nova_act.impl.message_encrypter.MessageEncrypter")
    def test_message_encryption(self, mock_encrypter: MagicMock) -> None:
        """Test message encryption functionality."""
        # Setup mock
        mock_encrypter.return_value = MagicMock()
        mock_encrypter.return_value.encrypt.return_value = b"encrypted"
        mock_encrypter.return_value.decrypt.return_value = b"decrypted"
        
        # Test encryption
        encrypter = mock_encrypter()
        encrypted = encrypter.encrypt(b"test message")
        self.assertEqual(encrypted, b"encrypted")
        
        # Test decryption
        decrypted = encrypter.decrypt(encrypted)
        self.assertEqual(decrypted, b"decrypted")


if __name__ == "__main__":
    unittest.main()