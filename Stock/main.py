"""
WSGI entry point for Azure App Service
"""
import os
import sys

# Add the application directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

if __name__ == "__main__":
    application.run()