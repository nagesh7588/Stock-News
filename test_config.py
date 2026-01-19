"""
Unit tests for the configuration module.
"""
import unittest
import os
from unittest.mock import patch


class TestConfig(unittest.TestCase):
    """Test cases for configuration."""

    @patch.dict(os.environ, {'NEWS_API_KEY': 'test_key_12345'})
    def test_config_with_api_key(self):
        """Test that config loads API key from environment."""
        # Need to reload module to pick up new environment
        import importlib
        import config
        importlib.reload(config)
        
        self.assertEqual(config.NEWS_API_KEY, 'test_key_12345')

    @patch.dict(os.environ, {}, clear=True)
    def test_config_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with self.assertRaises(ValueError) as context:
            import importlib
            import config
            importlib.reload(config)
        
        self.assertIn('NEWS_API_KEY', str(context.exception))

    @patch.dict(os.environ, {'NEWS_API_KEY': ''})
    def test_config_with_empty_api_key_raises_error(self):
        """Test that empty API key raises ValueError."""
        with self.assertRaises(ValueError) as context:
            import importlib
            import config
            importlib.reload(config)
        
        self.assertIn('NEWS_API_KEY', str(context.exception))


if __name__ == '__main__':
    unittest.main()
