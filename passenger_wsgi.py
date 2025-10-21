"""
WSGI entry point for cPanel/Passenger deployment.

This file is used by Passenger (cPanel/WHM) to run the Flask application.
"""
import sys
import os

# Add your project directory to the sys.path
project_home = os.path.dirname(__file__)
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import Flask app
from app import create_app

# Create application instance
application = create_app()

# For debugging only (remove in production)
if __name__ == '__main__':
    application.run()
