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
    try:
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
        
        if 'articles' not in data:
            return []
            
        articles = data.get("articles", [])
        if not articles:
            return []

        # Filter articles by keywords in title/description
        filtered = []
        for article in articles:
            if not article or not isinstance(article, dict):
                continue
                
            # Safely extract strings with guaranteed non-None values
            title = ""
            description = ""
            
            if article.get("title"):
                title = str(article.get("title"))
            if article.get("description"):
                description = str(article.get("description"))
            
            # Create search text - both are guaranteed to be strings now
            search_text = title + " " + description
            search_text = search_text.lower()
            
            # Check for keywords
            has_keyword = False
            for keyword in KEYWORDS:
                if keyword.lower() in search_text:
                    has_keyword = True
                    break
            
            if has_keyword:
                # Safe data extraction
                article_date = article.get("publishedAt", "")
                article_url = article.get("url", "#")
                
                # Safe source extraction
                source_name = "Unknown Source"
                source_obj = article.get("source")
                if source_obj and isinstance(source_obj, dict):
                    source_name = source_obj.get("name", "Unknown Source")
                
                # Determine date type
                date_type = "Publish Date"
                if (article_date and 
                    isinstance(article_date, str) and 
                    len(article_date) >= 10):
                    try:
                        pub_date = datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%SZ")
                        if (datetime.utcnow() - pub_date).days < 1:
                            date_type = "Recently Published Date"
                    except:
                        pass
                
                filtered.append({
                    "title": title if title else "No Title Available",
                    "date": article_date,
                    "source": source_name,
                    "description": description if description else "No description available",
                    "url": article_url,
                    "date_type": date_type
                })
        
        return filtered
        
    except Exception as e:
        # Return empty list on any error to prevent app crash
        return []
