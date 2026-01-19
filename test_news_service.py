"""
Unit tests for the news service module.
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import requests
import news_service


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions."""

    def test_extract_source_name_valid_dict(self):
        """Test extracting source name from valid dict."""
        source = {'id': 'bbc', 'name': 'BBC News'}
        result = news_service._extract_source_name(source)
        self.assertEqual(result, 'BBC News')

    def test_extract_source_name_none(self):
        """Test extracting source name when source is None."""
        result = news_service._extract_source_name(None)
        self.assertIsNone(result)

    def test_extract_source_name_empty_dict(self):
        """Test extracting source name from empty dict."""
        result = news_service._extract_source_name({})
        self.assertIsNone(result)

    def test_extract_source_name_missing_name(self):
        """Test extracting source name when name key is missing."""
        source = {'id': 'bbc'}
        result = news_service._extract_source_name(source)
        self.assertIsNone(result)

    def test_extract_source_name_invalid_type(self):
        """Test extracting source name from invalid type."""
        result = news_service._extract_source_name("invalid string")
        self.assertIsNone(result)

    def test_safe_get_text_valid_fields(self):
        """Test extracting text from valid article fields."""
        article = {
            'title': 'Stock Market News',
            'description': 'Market rises today'
        }
        result = news_service._safe_get_text(article, 'title', 'description')
        self.assertEqual(result, 'stock market news market rises today')

    def test_safe_get_text_missing_fields(self):
        """Test extracting text when fields are missing."""
        article = {'title': 'Stock News'}
        result = news_service._safe_get_text(article, 'title', 'description')
        self.assertEqual(result, 'stock news')

    def test_safe_get_text_none_values(self):
        """Test extracting text when values are None."""
        article = {'title': None, 'description': None}
        result = news_service._safe_get_text(article, 'title', 'description')
        self.assertEqual(result, '')

    def test_safe_get_text_non_string_values(self):
        """Test extracting text when values are not strings."""
        article = {'title': 123, 'description': ['list', 'data']}
        result = news_service._safe_get_text(article, 'title', 'description')
        self.assertEqual(result, '')

    def test_matches_keywords_found(self):
        """Test keyword matching when keyword is present."""
        text = 'stock market rises today'
        result = news_service._matches_keywords(text, ['stock', 'market'])
        self.assertTrue(result)

    def test_matches_keywords_not_found(self):
        """Test keyword matching when keyword is not present."""
        text = 'weather forecast sunny'
        result = news_service._matches_keywords(text, ['stock', 'market'])
        self.assertFalse(result)

    def test_matches_keywords_empty_text(self):
        """Test keyword matching with empty text."""
        result = news_service._matches_keywords('', ['stock'])
        self.assertFalse(result)

    def test_matches_keywords_case_insensitive(self):
        """Test keyword matching is case insensitive."""
        text = 'stock market news'  # Text should be lowercase
        result = news_service._matches_keywords(text, ['STOCK', 'MARKET'])
        self.assertTrue(result)


class TestNewsService(unittest.TestCase):
    """Test cases for news service functions."""

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_success(self, mock_get):
        """Test successful news fetching and filtering."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Stock Market Rises',
                    'description': 'Stocks are up today',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Financial Times'},
                    'url': 'https://example.com/news1'
                },
                {
                    'title': 'Weather Update',
                    'description': 'Sunny day ahead',
                    'publishedAt': '2026-01-19T09:00:00Z',
                    'source': {'name': 'Weather News'},
                    'url': 'https://example.com/news2'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should only return stock-related news
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Stock Market Rises')
        self.assertEqual(result[0]['source'], 'Financial Times')
        mock_get.assert_called_once()

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_null_source(self, mock_get):
        """Test handling of null source values."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Stock Market Update',
                    'description': 'Market news',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': None,  # Null source
                    'url': 'https://example.com/news1'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should handle null source gracefully
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]['source'])
        self.assertEqual(result[0]['title'], 'Stock Market Update')

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_missing_source_name(self, mock_get):
        """Test handling of source dict without name field."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Earnings Report for stocks',
                    'description': 'Quarterly results',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'id': 'business-wire'},  # Missing 'name'
                    'url': 'https://example.com/news1'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]['source'])

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_all_fields_null(self, mock_get):
        """Test handling of article with all null fields."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Stock',  # Must have keyword to be included
                    'description': None,
                    'publishedAt': None,
                    'source': None,
                    'url': None
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Stock')
        self.assertIsNone(result[0]['description'])
        self.assertIsNone(result[0]['source'])
        self.assertIsNone(result[0]['date'])
        self.assertIsNone(result[0]['url'])

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_empty_response(self, mock_get):
        """Test handling of empty API response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'articles': []}
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        self.assertEqual(result, [])
        mock_get.assert_called_once()

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_malformed_article(self, mock_get):
        """Test handling of malformed article objects."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                "not a dict",  # Malformed article
                {
                    'title': 'Stock Market News',
                    'description': 'Valid article',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Finance'},
                    'url': 'https://example.com/news'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should skip malformed article and process valid one
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Stock Market News')

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        mock_get.side_effect = requests.HTTPError("404 Not Found")

        with self.assertRaises(requests.RequestException):
            news_service.fetch_filtered_news()

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_timeout(self, mock_get):
        """Test handling of request timeout."""
        mock_get.side_effect = requests.Timeout("Request timed out")

        with self.assertRaises(requests.RequestException):
            news_service.fetch_filtered_news()

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_invalid_json(self, mock_get):
        """Test handling of invalid JSON response."""
        mock_response = MagicMock()
        mock_response.json.return_value = "not a dict"
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            news_service.fetch_filtered_news()

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_invalid_articles_type(self, mock_get):
        """Test handling when articles field is not a list."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'articles': "not a list"}
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            news_service.fetch_filtered_news()

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_filters_by_keywords(self, mock_get):
        """Test that news is properly filtered by keywords."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Sensex hits new high',
                    'description': 'Market rally continues',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Economic Times'},
                    'url': 'https://example.com/news1'
                },
                {
                    'title': 'Nifty crosses 20000',
                    'description': 'Share market bullish',
                    'publishedAt': '2026-01-19T09:00:00Z',
                    'source': {'name': 'Business Standard'},
                    'url': 'https://example.com/news2'
                },
                {
                    'title': 'Sports news',
                    'description': 'Team wins championship',
                    'publishedAt': '2026-01-19T08:00:00Z',
                    'source': {'name': 'Sports Daily'},
                    'url': 'https://example.com/news3'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        # Should return 2 stock-related articles, not the sports one
        self.assertEqual(len(result), 2)
        titles = [article['title'] for article in result]
        self.assertIn('Sensex hits new high', titles)
        self.assertIn('Nifty crosses 20000', titles)
        self.assertNotIn('Sports news', titles)

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_case_insensitive_filtering(self, mock_get):
        """Test that keyword filtering is case-insensitive."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'STOCK MARKET NEWS',
                    'description': 'EARNINGS report',
                    'publishedAt': '2026-01-19T10:00:00Z',
                    'source': {'name': 'Finance News'},
                    'url': 'https://example.com/news1'
                }
            ]
        }
        mock_get.return_value = mock_response

        result = news_service.fetch_filtered_news()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'STOCK MARKET NEWS')

    @patch('news_service.requests.get')
    @patch('news_service.NEWS_API_KEY', 'test_api_key')
    def test_fetch_filtered_news_timeout_parameter(self, mock_get):
        """Test that timeout is set on API requests."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'articles': []}
        mock_get.return_value = mock_response

        news_service.fetch_filtered_news()

        # Verify timeout was set
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['timeout'], 10)


class TestFilterKeywords(unittest.TestCase):
    """Test cases for filter keywords."""

    def test_filter_keywords_exist(self):
        """Test that filter keywords are defined."""
        self.assertIsInstance(news_service.FILTER_KEYWORDS, list)
        self.assertGreater(len(news_service.FILTER_KEYWORDS), 0)

    def test_filter_keywords_content(self):
        """Test that essential keywords are present."""
        keywords_lower = [kw.lower() for kw in news_service.FILTER_KEYWORDS]
        self.assertIn('stock', keywords_lower)
        self.assertIn('market', keywords_lower)


if __name__ == '__main__':
    unittest.main()
