import requests
from datetime import datetime, timedelta
from config import NEWS_API_KEY

# Keywords to filter news articles
KEYWORDS = [
    "stock"
]

NEWS_API_URL = "https://newsapi.org/v2/everything"


def fetch_stock_news():
    """
    Fetch news articles from the last 24 hours containing stock market keywords.
    Returns a list of filtered articles.
    """
    now = datetime.utcnow()
    from_date = (now - timedelta(days=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
    to_date = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Build query string for keywords
    query = " OR ".join([f'"{kw}"' for kw in KEYWORDS])

    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY,
        "pageSize": 50
    }

    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    print("Raw API response:", data)  # Debug: print raw response
    articles = data.get("articles", [])
    print(f"Articles returned by API: {len(articles)}")  # Debug: print count

    # Filter articles by keywords in title/description
    filtered = []
    for article in articles:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        if any(kw in text for kw in KEYWORDS):
            filtered.append({
                "title": article.get("title"),
                "date": article.get("publishedAt"),
                "source": article.get("source", {}).get("name"),
                "description": article.get("description"),
                "url": article.get("url")
            })
    return filtered
