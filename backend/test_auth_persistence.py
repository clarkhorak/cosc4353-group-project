import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.auth_service import AuthService
from app.models.user import UserCreate, UserLogin
from app.models.database import User

class TestAuthPersistence:
    """Test user persistence in database"""
    
    def setup_method(self):
        """Setup test environment"""
        self.auth_service = AuthService()
    
    @patch('app.repositories.user_repository.UserRepository')
    def test_register_user_persists_to_database(self, mock_repo):
        """Test that user registration persists to database"""
        # Mock the repository
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock that user doesn't exist initially
        mock_repo_instance.get_by_email.return_value = None
        
        # Mock the created user
        mock_db_user = MagicMock()
        mock_db_user.id = "test-user-id"
        mock_db_user.email = "test@example.com"
        mock_db_user.full_name = "Test User"
        mock_db_user.created_at = "2024-01-01T00:00:00"
        mock_db_user.is_active = True
        mock_repo_instance.create.return_value = mock_db_user
        
        # Create test user data
        user_data = UserCreate(
            email="test@example.com",
            full_name="Test User",
            password="TestPassword123"
        )
        
        # Register user
        user = self.auth_service.register_user(user_data)
        
        # Verify repository methods were called
        mock_repo_instance.get_by_email.assert_called_once_with("test@example.com")
        mock_repo_instance.create.assert_called_once()
        
        # Verify user was created with correct data
        create_call_args = mock_repo_instance.create.call_args[1]
        assert create_call_args["email"] == "test@example.com"
        assert create_call_args["full_name"] == "Test User"
        assert create_call_args["is_active"] == True
        assert "hashed_password" in create_call_args
        
        # Verify returned user object
        assert user.id == "test-user-id"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active == True
    
    @patch('app.repositories.user_repository.UserRepository')
    def test_authenticate_user_from_database(self, mock_repo):
        """Test that user authentication reads from database"""
        # Mock the repository
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock existing user in database
        mock_db_user = MagicMock()
        mock_db_user.email = "test@example.com"
        mock_db_user.hashed_password = "$2b$12$test_hash"  # Mock bcrypt hash
        mock_db_user.is_active = True
        mock_repo_instance.get_by_email.return_value = mock_db_user
        
        # Mock password verification
        with patch.object(self.auth_service, 'verify_password', return_value=True):
            # Create login data
            login_data = UserLogin(
                email="test@example.com",
                password="TestPassword123"
            )
            
            # Authenticate user
            token = self.auth_service.authenticate_user(login_data)
            
            # Verify repository was called
            mock_repo_instance.get_by_email.assert_called_once_with("test@example.com")
            
            # Verify token was created
            assert token is not None
    
    @patch('app.repositories.user_repository.UserRepository')
    def test_user_not_found_in_database(self, mock_repo):
        """Test authentication fails when user doesn't exist in database"""
        # Mock the repository
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        
        # Mock that user doesn't exist
        mock_repo_instance.get_by_email.return_value = None
        
        # Create login data
        login_data = UserLogin(
            email="nonexistent@example.com",
            password="TestPassword123"
        )
        
        # Authenticate user
        token = self.auth_service.authenticate_user(login_data)
        
        # Verify authentication failed
        assert token is None
        
        # Verify repository was called
        mock_repo_instance.get_by_email.assert_called_once_with("nonexistent@example.com")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 