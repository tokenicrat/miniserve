#!/usr/bin/env python3
"""
WSGI entry point for the object storage application.
This file provides the WSGI callable that Gunicorn will use.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the Flask application
from app import app

# WSGI callable
application = app

if __name__ == "__main__":
    # For development/testing
    application.run(host='0.0.0.0', port=5000, debug=False)
