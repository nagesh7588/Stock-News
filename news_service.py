"""
Service to fetch and filter stock/share market news from NewsAPI.org.
"""
import os
import requests
from datetime import datetime, timedelta
from config import NEWS_API_KEY

FILTER_KEYWORDS = [
    "stock", "stocks", "share market", "sensex", "nifty", "market", "earnings", "quarter results"
]

NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_filtered_news():
    """
    Fetch news from the last 24 hours and filter by keywords.
    Returns a list of dicts with title, date, source, description, and url.
    """
    now = datetime.utcnow()
    from_date = (now - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        'q': ' OR '.join(FILTER_KEYWORDS),
        'from': from_date,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': NEWS_API_KEY,
        'pageSize': 50
    }
    response = requests.get(NEWS_API_URL, params=params)
    articles = response.json().get('articles', [])
    filtered = []
    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        if any(kw in text for kw in FILTER_KEYWORDS):
            filtered.append({
                'title': article.get('title'),
                'date': article.get('publishedAt'),
                'source': article.get('source', {}).get('name'),
                'description': article.get('description'),
                'url': article.get('url')
            })
    return filtered
