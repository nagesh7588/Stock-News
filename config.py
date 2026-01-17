"""
Configuration for News API key via environment variable.
"""
import os

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY environment variable not set.")
