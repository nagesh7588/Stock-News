import os

# Load News API key from environment variable
"""
Configuration file for News API key.
"""
# Directly set the News API key as provided by the user.
NEWS_API_KEY = "96253f376c4c4e0ea111e78676cf3de3"

if not NEWS_API_KEY:
    raise ValueError('NEWS_API_KEY environment variable not set.')
