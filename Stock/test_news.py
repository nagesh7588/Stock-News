#!/usr/bin/env python3
"""
Test script to verify the news service works without errors
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from news_service import fetch_stock_news

def test_news_service():
    try:
        print("Testing news service...")
        articles = fetch_stock_news()
        print(f"✅ Successfully fetched {len(articles)} articles")
        
        if articles:
            print("Sample article:")
            article = articles[0]
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Source: {article.get('source', 'N/A')}")
            print(f"  Date: {article.get('date', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_news_service()