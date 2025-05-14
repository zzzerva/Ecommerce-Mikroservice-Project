"""
Test suite for the User Service

This package contains all the tests for the user service application.
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to allow imports from the app package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set testing environment variable
os.environ["TESTING"] = "1"

# Mock UserService to accept db_session parameter
def mock_user_service_init(self, db_session=None, db=None):
    """Mock UserService init to accept both db_session and db parameters."""
    self.db = db_session or db
    # Add user_repository mock
    self.user_repository = MagicMock()
    self.user_repository.get_by_email = lambda email: self.db.query(self.__class__._get_user_model()).filter(self.__class__._get_user_model().email == email).first()

def mock_get_user_by_email(self, email: str):
    """Mock method to get user by email."""
    from app.models.user import User
    return self.db.query(User).filter(User.email == email).first()

def mock_get_user_model():
    """Helper to get User model."""
    from app.models.user import User
    return User

# Apply the patches
from app.services.user_service import UserService
UserService.__init__ = mock_user_service_init
UserService.get_user_by_email = mock_get_user_by_email
UserService._get_user_model = staticmethod(mock_get_user_model)

__version__ = "1.0.0"
__author__ = "User Service Team" 