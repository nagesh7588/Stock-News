import os

# Load News API key from environment variable or use default
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '96253f376c4c4e0ea111e78676cf3de3')

if not NEWS_API_KEY:
    raise ValueError('NEWS_API_KEY environment variable not set.')
