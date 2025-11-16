from flask import Flask, render_template
from news_service import fetch_stock_news

app = Flask(__name__)

@app.route('/')
def index():
    """
    Home page route. Fetches and displays filtered stock/share market news.
    """
    try:
        articles = fetch_stock_news()
    except Exception as e:
        articles = []
        error = str(e)
    else:
        error = None
    return render_template('index.html', articles=articles, error=error)

if __name__ == '__main__':
    # For local development only
    app.run(debug=True)
