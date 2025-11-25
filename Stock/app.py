from flask import Flask, render_template
import os
import sys

# Add error handling for imports
try:
    from news_service import fetch_stock_news
except ImportError as e:
    print(f"Import error: {e}")
    def fetch_stock_news():
        return []

app = Flask(__name__)

@app.route('/')
def index():
    """
    Home page route. Fetches and displays filtered stock/share market news.
    """
    try:
        articles = fetch_stock_news()
    except Exception as e:
        print(f"Error fetching news: {e}")
        articles = []
        error = str(e)
    else:
        error = None
    return render_template('index.html', articles=articles, error=error)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "python_path": sys.path[:3]}

if __name__ == '__main__':
    # For local development only
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
