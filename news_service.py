"""
Service to fetch and filter stock/share market news from NewsAPI.org.
"""
import os
import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Any
from config import NEWS_API_KEY

FILTER_KEYWORDS = [
    "stock", "stocks", "share market", "sensex", "nifty", "market", "earnings", "quarter results"
]

NEWS_API_URL = "https://newsapi.org/v2/everything"


def _extract_source_name(source: Any) -> Optional[str]:
    """
    Safely extract source name from article source field.
    
    Args:
        source: Source object from API response (can be dict, None, or other)
        
    Returns:
        Source name as string, or None if unavailable
    """
    if source is None:
        return None
    
    if isinstance(source, dict):
        return source.get('name')
    
    # Handle unexpected types gracefully
    return None


def _safe_get_text(article: Dict[str, Any], *keys: str) -> str:
    """
    Safely extract and concatenate text fields from article.
    
    Args:
        article: Article dictionary
        *keys: Keys to extract and concatenate
        
    Returns:
        Concatenated lowercase string, or empty string if all fields are None/missing
    """
    text_parts = []
    for key in keys:
        value = article.get(key)
        if value is not None and isinstance(value, str):
            text_parts.append(value)
    
    return ' '.join(text_parts).lower()


def _matches_keywords(text: str, keywords: List[str]) -> bool:
    """
    Check if text contains any of the filter keywords.
    
    Args:
        text: Text to search (should be lowercase)
        keywords: List of keywords to search for
        
    Returns:
        True if any keyword found, False otherwise
    """
    if not text:
        return False
    
    return any(keyword.lower() in text for keyword in keywords)


def fetch_filtered_news() -> List[Dict[str, Optional[str]]]:
    """
    Fetch news from the last 24 hours and filter by keywords.
    
    Returns:
        List of dicts with title, date, source, description, and url.
        Returns empty list on API errors.
        
    Raises:
        requests.RequestException: If API request fails
        ValueError: If API response is invalid
    """
    try:
        # Use timezone-aware datetime (fixes deprecation warning)
        now = datetime.now(timezone.utc)
        from_date = (now - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        params = {
            'q': ' OR '.join(FILTER_KEYWORDS),
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': NEWS_API_KEY,
            'pageSize': 50
        }
        
        # Make API request
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse JSON response
        data = response.json()
        
        if not isinstance(data, dict):
            raise ValueError("Invalid API response format: expected dict")
        
        articles = data.get('articles', [])
        
        if not isinstance(articles, list):
            raise ValueError("Invalid articles format: expected list")
        
        filtered = []
        
        for article in articles:
            if not isinstance(article, dict):
                continue  # Skip malformed articles
            
            # Extract text for keyword matching
            text = _safe_get_text(article, 'title', 'description')
            
            # Check if article matches keywords
            if _matches_keywords(text, FILTER_KEYWORDS):
                # Safely extract all fields
                filtered.append({
                    'title': article.get('title'),
                    'date': article.get('publishedAt'),
                    'source': _extract_source_name(article.get('source')),
                    'description': article.get('description'),
                    'url': article.get('url')
                })
        
        return filtered
        
    except requests.RequestException as e:
        # Log error in production
        print(f"API request failed: {e}")
        raise
    except (ValueError, KeyError) as e:
        # Log error in production
        print(f"Invalid API response: {e}")
        raise
