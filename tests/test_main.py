"""Tests for the main module."""

import os
import tempfile
import unittest
import json
from unittest.mock import patch

from nova_act.main import load_config, setup_logging


class TestMain(unittest.TestCase):
    """Test cases for the main module."""

    def test_load_config(self):
        """Test loading configuration from a file."""
        test_config = {
            "environment": "test",
            "logging": {"level": "debug"}
        }
        
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
            json.dump(test_config, temp)
            temp_name = temp.name
        
        try:
            # Test loading the config
            config = load_config(temp_name)
            self.assertEqual(config, test_config)
            self.assertEqual(config["environment"], "test")
            self.assertEqual(config["logging"]["level"], "debug")
        finally:
            # Clean up
            os.unlink(temp_name)
    
    @patch('logging.basicConfig')
    def test_setup_logging(self, mock_basic_config):
        """Test setting up logging with different log levels."""
        # Test with debug level
        setup_logging("debug")
        mock_basic_config.assert_called_once()
        
        # Reset mock
        mock_basic_config.reset_mock()
        
        # Test with info level
        setup_logging("info")
        mock_basic_config.assert_called_once()
        
        # Test with invalid level should raise ValueError
        with self.assertRaises(ValueError):
            setup_logging("invalid_level")


if __name__ == "__main__":
    unittest.main() 