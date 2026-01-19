"""
Integration tests for Stock News application.
Tests interaction between Flask app, news service, and config modules.
"""
import unittest
import os
from unittest.mock import patch, MagicMock
import json


class TestFlaskNewsServiceIntegration(unittest.TestCase):
    """Integration tests between Flask app and news service."""

    def setUp(self):
        """Set up test environment."""
        os.environ['NEWS_API_KEY'] = 'test_integration_key'
        
        # Reload modules to pick up env var
        import importlib
        import config
        import news_service
        importlib.reload(config)
        importlib.reload(news_service)
        
        # Import after setting env var
        from app import app
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after tests."""
        if 'NEWS_API_KEY' in os.environ:
            del os.environ['NEWS_API_KEY']

    @patch('news_service.requests.get')
    def test_end_to_end_news_flow(self, mock_get):
        """Test complete flow from API call to rendered page."""
        # Mock NewsAPI response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Sensex reaches new high',
                    'description': 'Stock market shows strong performance',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Economic Times'},
                    'url': 'https://example.com/news1'
                },
                {
                    'title': 'Nifty crosses 20000',
                    'description': 'Share market continues upward trend',
                    'publishedAt': '2026-01-19T09:30:00Z',
                    'source': {'name': 'Business Standard'},
                    'url': 'https://example.com/news2'
                }
            ]
        }
        mock_get.return_value = mock_response

        # Make request to Flask app
        response = self.client.get('/')

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sensex reaches new high', response.data)
        self.assertIn(b'Nifty crosses 20000', response.data)
        self.assertIn(b'Economic Times', response.data)
        
        # Verify API was called with correct parameters
        call_args = mock_get.call_args
        params = call_args[1]['params']
        self.assertEqual(params['apiKey'], 'test_integration_key')
        self.assertIn('stock', params['q'].lower())

    @patch('news_service.requests.get')
    def test_filtering_integration(self, mock_get):
        """Test that filtering works correctly in full flow."""
        # Mock response with mixed content
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Stock Market Update',
                    'description': 'Stocks rise today',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Financial Times'},
                    'url': 'https://example.com/news1'
                },
                {
                    'title': 'Sports Championship',
                    'description': 'Team wins final match',
                    'publishedAt': '2026-01-19T09:00:00Z',
                    'source': {'name': 'Sports News'},
                    'url': 'https://example.com/news2'
                },
                {
                    'title': 'Earnings Report Released',
                    'description': 'Company shows profit growth',
                    'publishedAt': '2026-01-19T08:00:00Z',
                    'source': {'name': 'Business Wire'},
                    'url': 'https://example.com/news3'
                }
            ]
        }
        mock_get.return_value = mock_response

        response = self.client.get('/')

        # Only stock-related news should appear
        self.assertIn(b'Stock Market Update', response.data)
        self.assertIn(b'Earnings Report Released', response.data)
        self.assertNotIn(b'Sports Championship', response.data)

    @patch('news_service.requests.get')
    def test_error_propagation(self, mock_get):
        """Test that errors from news service propagate to Flask app."""
        # Simulate API error
        mock_get.side_effect = Exception('API connection failed')

        with self.assertRaises(Exception) as context:
            response = self.client.get('/')
        
        self.assertIn('API connection failed', str(context.exception))

    @patch('news_service.requests.get')
    def test_empty_results_integration(self, mock_get):
        """Test handling of empty results through full stack."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'articles': []}
        mock_get.return_value = mock_response

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        # Page should still render even with no news


class TestNewsServiceConfigIntegration(unittest.TestCase):
    """Integration tests between news service and config."""

    def setUp(self):
        """Set up test environment."""
        os.environ['NEWS_API_KEY'] = 'integration_test_key_12345'

    def tearDown(self):
        """Clean up after tests."""
        if 'NEWS_API_KEY' in os.environ:
            del os.environ['NEWS_API_KEY']

    @patch('news_service.requests.get')
    def test_config_api_key_used_in_service(self, mock_get):
        """Test that news service correctly uses API key from config."""
        # Need to reload modules to pick up new env var
        import importlib
        import config
        import news_service
        importlib.reload(config)
        importlib.reload(news_service)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Market News',
                    'description': 'Stocks update',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Finance'},
                    'url': 'https://example.com/news1'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Verify API key from config was used
        call_args = mock_get.call_args
        params = call_args[1]['params']
        self.assertEqual(params['apiKey'], 'integration_test_key_12345')

    def test_config_missing_key_prevents_service(self):
        """Test that missing config API key prevents service from working."""
        # Remove API key
        del os.environ['NEWS_API_KEY']

        # Attempting to reload config should raise error
        with self.assertRaises(ValueError):
            import importlib
            import config
            importlib.reload(config)


class TestAPIResponseHandling(unittest.TestCase):
    """Integration tests for API response handling."""

    def setUp(self):
        """Set up test environment."""
        os.environ['NEWS_API_KEY'] = 'test_key'

    def tearDown(self):
        """Clean up after tests."""
        if 'NEWS_API_KEY' in os.environ:
            del os.environ['NEWS_API_KEY']

    @patch('news_service.requests.get')
    def test_malformed_api_response(self, mock_get):
        """Test handling of malformed API responses."""
        import importlib
        import news_service
        importlib.reload(news_service)

        # Mock malformed response
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # Missing 'articles' key
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should return empty list, not crash
        self.assertEqual(result, [])

    @patch('news_service.requests.get')
    def test_partial_article_data(self, mock_get):
        """Test handling of articles with partial data."""
        import importlib
        import news_service
        importlib.reload(news_service)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Stock market rises',
                    # Missing description, source, url
                    'publishedAt': '2026-01-19T10:00:00Z'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should still process the article
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Stock market rises')
        self.assertIsNone(result[0]['description'])
        self.assertIsNone(result[0]['source'])

    @patch('news_service.requests.get')
    def test_date_formatting_integration(self, mock_get):
        """Test that dates are properly handled through the stack."""
        import importlib
        import news_service
        importlib.reload(news_service)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Market update with stocks',
                    'description': 'Latest news',
                    'publishedAt': '2026-01-19T14:30:00Z',
                    'source': {'name': 'Finance'},
                    'url': 'https://example.com/news'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Verify date is preserved
        self.assertEqual(result[0]['date'], '2026-01-19T14:30:00Z')

    @patch('news_service.requests.get')
    def test_keyword_matching_integration(self, mock_get):
        """Test keyword matching with various formats."""
        import importlib
        import news_service
        importlib.reload(news_service)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'SENSEX Analysis',
                    'description': 'Index rises',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'ET'},
                    'url': 'https://example.com/1'
                },
                {
                    'title': 'Tech News',
                    'description': 'New product launch',
                    'publishedAt': '2026-01-19T09:00:00Z',
                    'source': {'name': 'Tech'},
                    'url': 'https://example.com/2'
                },
                {
                    'title': 'Company Earnings',
                    'description': 'Quarterly results announced',
                    'publishedAt': '2026-01-19T08:00:00Z',
                    'source': {'name': 'Business'},
                    'url': 'https://example.com/3'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should match SENSEX (case-insensitive) and earnings
        self.assertEqual(len(result), 2)
        titles = [r['title'] for r in result]
        self.assertIn('SENSEX Analysis', titles)
        self.assertIn('Company Earnings', titles)


class TestFullStackIntegration(unittest.TestCase):
    """Full stack integration tests."""

    def setUp(self):
        """Set up test environment."""
        os.environ['NEWS_API_KEY'] = 'full_stack_test_key'
        
        from app import app
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after tests."""
        if 'NEWS_API_KEY' in os.environ:
            del os.environ['NEWS_API_KEY']

    @patch('news_service.requests.get')
    def test_complete_user_flow(self, mock_get):
        """Simulate complete user interaction flow."""
        # Mock realistic API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'ok',
            'totalResults': 2,
            'articles': [
                {
                    'source': {'id': 'economic-times', 'name': 'Economic Times'},
                    'author': 'Market Reporter',
                    'title': 'Sensex jumps 500 points on strong earnings',
                    'description': 'Stock market shows robust performance',
                    'url': 'https://economictimes.com/market-news',
                    'urlToImage': 'https://example.com/image.jpg',
                    'publishedAt': '2026-01-19T12:30:00Z',
                    'content': 'Full article content here...'
                },
                {
                    'source': {'id': None, 'name': 'Business Standard'},
                    'author': 'Finance Desk',
                    'title': 'Nifty crosses 20,000 mark amid positive sentiment',
                    'description': 'Share market reaches milestone',
                    'url': 'https://business-standard.com/market',
                    'urlToImage': 'https://example.com/image2.jpg',
                    'publishedAt': '2026-01-19T11:45:00Z',
                    'content': 'Market analysis content...'
                }
            ]
        }
        mock_get.return_value = mock_response

        # User visits homepage
        response = self.client.get('/')

        # Verify successful response
        self.assertEqual(response.status_code, 200)
        
        # Verify news content is displayed
        self.assertIn(b'Sensex jumps 500 points', response.data)
        self.assertIn(b'Nifty crosses 20,000 mark', response.data)
        self.assertIn(b'Economic Times', response.data)
        self.assertIn(b'Business Standard', response.data)

        # Verify API integration
        self.assertTrue(mock_get.called)
        call_args = mock_get.call_args
        self.assertEqual(call_args[0][0], 'https://newsapi.org/v2/everything')


if __name__ == '__main__':
    unittest.main()
