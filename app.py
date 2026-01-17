"""
Flask app for displaying filtered stock/share market news from the last 24 hours.
"""
import os
from flask import Flask, render_template
from news_service import fetch_filtered_news

app = Flask(__name__)

@app.route('/')
def index():
    news = fetch_filtered_news()
    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run(debug=True)
