"""
Test suite for the User Service

This package contains all the tests for the user service application.
"""

import os
import sys

# Add the parent directory to the path to allow imports from the app package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set testing environment variable
os.environ["TESTING"] = "1"

__version__ = "1.0.0"
__author__ = "User Service Team" 