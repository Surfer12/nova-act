"""Test package imports work correctly."""
import unittest

class TestImports(unittest.TestCase):
    """Test that all public package imports work."""

    def test_imports(self):
        """Test importing public package members."""
        from nova_act import (
            NovaAct,
            BridgeClient,
            NovaBridgeServer,
            ActResult,
            setup_logging,
            load_config
        )
        self.assertIsNotNone(NovaAct)
        self.assertIsNotNone(BridgeClient)
        self.assertIsNotNone(NovaBridgeServer)
        self.assertIsNotNone(ActResult)
        self.assertIsNotNone(setup_logging)
        self.assertIsNotNone(load_config)
        
        # Test that version is available
        from nova_act import __version__
        self.assertIsNotNone(__version__)