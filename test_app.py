"""
Unit tests for the Flask application.
"""
import unittest
from unittest.mock import patch, MagicMock
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask routes."""

    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('app.fetch_filtered_news')
    def test_index_route_success(self, mock_fetch_news):
        """Test that index route renders successfully with news data."""
        # Mock news data
        mock_news = [
            {
                'title': 'Stock Market Update',
                'date': '2026-01-19T10:00:00Z',
                'source': 'Financial Times',
                'description': 'Markets rally today',
                'url': 'https://example.com/news1'
            }
        ]
        mock_fetch_news.return_value = mock_news

        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stock Market Update', response.data)
        mock_fetch_news.assert_called_once()

    @patch('app.fetch_filtered_news')
    def test_index_route_empty_news(self, mock_fetch_news):
        """Test index route when no news is available."""
        mock_fetch_news.return_value = []

        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        mock_fetch_news.assert_called_once()

    @patch('app.fetch_filtered_news')
    def test_index_route_handles_exception(self, mock_fetch_news):
        """Test that index route handles exceptions gracefully."""
        mock_fetch_news.side_effect = Exception('API Error')

        with self.assertRaises(Exception):
            response = self.client.get('/')


if __name__ == '__main__':
    unittest.main()
