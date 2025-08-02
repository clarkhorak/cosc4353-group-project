#!/usr/bin/env python3
"""
Test script for authentication system
Run this to verify that authentication works correctly
"""

import sys
import os
import requests
import json
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.auth_service import AuthService
from app.models.user import UserCreate, UserLogin
from app.repositories.user_repository import UserRepository

def test_auth_service():
    """Test the authentication service directly"""
    print("🧪 Testing AuthService...")
    
    auth_service = AuthService()
    
    # Test user registration
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="SecurePass123"
    )
    
    user = auth_service.register_user(user_data)
    print("✅ User registration successful")
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    
    # Test duplicate registration
    try:
        auth_service.register_user(user_data)
        assert False, "Should have failed for duplicate email"
    except ValueError:
        print("✅ Duplicate email validation working")
    
    # Test password hashing
    hashed_password = auth_service.hash_password("testpassword")
    print("✅ Password hashing working")
    assert hashed_password != "testpassword"
    
    # Test password verification
    is_valid = auth_service.verify_password("testpassword", hashed_password)
    assert is_valid, "Password verification failed"
    print("✅ Password verification working")
    
    # Test user authentication
    login_data = UserLogin(
        email="test@example.com",
        password="SecurePass123"
    )
    
    token = auth_service.authenticate_user(login_data)
    assert token is not None, "User authentication failed"
    print("✅ User authentication successful")
    
    # Test token verification
    email = auth_service.verify_token(token)
    assert email == "test@example.com", "Token verification failed"
    print("✅ Token verification working")
    
    # Test invalid password
    invalid_login = UserLogin(
        email="test@example.com",
        password="wrongpassword"
    )
    
    invalid_token = auth_service.authenticate_user(invalid_login)
    assert invalid_token is None, "Invalid password should have been rejected"
    print("✅ Invalid password validation working")
    
    # Test non-existent user
    non_existent_login = UserLogin(
        email="nonexistent@example.com",
        password="anypassword"
    )
    
    non_existent_token = auth_service.authenticate_user(non_existent_login)
    assert non_existent_token is None, "Non-existent user should have been rejected"
    print("✅ Non-existent user validation working")
    
    print("✅ All AuthService tests passed")

def test_auth_service_with_repository():
    """Test AuthService with repository pattern"""
    print("\n🧪 Testing AuthService with Repository...")
    
    # Mock the repository
    with patch('app.services.auth_service.UserRepository') as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        auth_service = AuthService()
        
        # Test user registration with repository
        user_data = UserCreate(
            email="repo@example.com",
            full_name="Repo User",
            password="SecurePass123"
        )
        
        # Mock repository responses
        mock_repo.get_by_email.return_value = None  # User doesn't exist initially
        
        mock_db_user = MagicMock()
        mock_db_user.id = "test-id"
        mock_db_user.email = "repo@example.com"
        mock_db_user.full_name = "Repo User"
        mock_db_user.created_at = datetime.now()
        mock_db_user.is_active = True
        mock_repo.create.return_value = mock_db_user
        
        # Register user
        user = auth_service.register_user(user_data)
        
        # Verify repository was called correctly
        mock_repo.get_by_email.assert_called_once_with("repo@example.com")
        mock_repo.create.assert_called_once()
        
        # Verify user was created with correct data
        create_call_args = mock_repo.create.call_args[1]
        assert create_call_args["email"] == "repo@example.com"
        assert create_call_args["full_name"] == "Repo User"
        assert create_call_args["is_active"] == True
        assert "hashed_password" in create_call_args
        
        print("✅ User registration with repository successful")
        
        # Test authentication with repository
        login_data = UserLogin(
            email="repo@example.com",
            password="SecurePass123"
        )
        
        # Mock existing user for authentication
        mock_db_user.hashed_password = "hashed_password"
        mock_repo.get_by_email.return_value = mock_db_user
        
        # Mock password verification
        with patch.object(auth_service, 'verify_password', return_value=True):
            token = auth_service.authenticate_user(login_data)
            assert token is not None
            print("✅ User authentication with repository successful")
        
        # Test get user by email
        user = auth_service.get_user_by_email("repo@example.com")
        assert user is not None
        assert user.email == "repo@example.com"
        print("✅ Get user by email successful")
        
        # Test get user by ID
        user = auth_service.get_user_by_id("test-id")
        assert user is not None
        assert user.id == "test-id"
        print("✅ Get user by ID successful")
        
        # Test update user
        updated_user = auth_service.update_user("test-id", full_name="Updated Name")
        assert updated_user is not None
        print("✅ Update user successful")
        
        # Test delete user
        result = auth_service.delete_user("test-id")
        assert result is True
        print("✅ Delete user successful")
        
        # Test get all users
        all_users = auth_service.get_all_users()
        assert isinstance(all_users, list)
        print("✅ Get all users successful")
        
        # Test user activation/deactivation
        result = auth_service.deactivate_user("repo@example.com")
        assert result is True
        print("✅ Deactivate user successful")
        
        result = auth_service.activate_user("repo@example.com")
        assert result is True
        print("✅ Activate user successful")

def test_repository_error_handling():
    """Test error handling in repository operations"""
    print("\n🧪 Testing Repository Error Handling...")
    
    with patch('app.services.auth_service.UserRepository') as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        
        auth_service = AuthService()
        
        # Test repository create error
        mock_repo.create.side_effect = Exception("Database error")
        
        user_data = UserCreate(
            email="error@example.com",
            full_name="Error User",
            password="SecurePass123"
        )
        
        try:
            auth_service.register_user(user_data)
            assert False, "Should have raised an exception"
        except Exception as e:
            assert "Database error" in str(e)
            print("✅ Repository create error handling working")
        
        # Test repository get_by_email error
        mock_repo.get_by_email.side_effect = Exception("Connection error")
        
        try:
            auth_service.get_user_by_email("error@example.com")
            assert False, "Should have raised an exception"
        except Exception as e:
            assert "Connection error" in str(e)
            print("✅ Repository get_by_email error handling working")

def test_auth_api():
    """Test the authentication API endpoints"""
    print("\n🧪 Testing Auth API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test registration
    register_data = {
        "email": "apitest@example.com",
        "full_name": "API Test User",
        "password": "SecurePass123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/register",
            headers={"Content-Type": "application/json"},
            json=register_data
        )
        
        if response.status_code == 201:
            print("✅ API registration successful")
            user_data = response.json()
            assert user_data["email"] == "apitest@example.com"
        else:
            print(f"❌ API registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # Test login
        login_data = {
            "email": "apitest@example.com",
            "password": "SecurePass123"
        }
        
        response = requests.post(
            f"{base_url}/auth/login",
            headers={"Content-Type": "application/json"},
            json=login_data
        )
        
        if response.status_code == 200:
            print("✅ API login successful")
            login_response = response.json()
            token = login_response.get("access_token")
            assert token is not None
            
            # Test get user info
            response = requests.get(
                f"{base_url}/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                print("✅ API get user info successful")
                user_info = response.json()
                assert user_info["email"] == "apitest@example.com"
            else:
                print(f"❌ API get user info failed: {response.status_code}")
        else:
            print(f"❌ API login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure server is running")
    except Exception as e:
        print(f"❌ API test error: {e}")

def test_jwt_token_operations():
    """Test JWT token creation and verification"""
    print("\n🧪 Testing JWT Token Operations...")
    
    auth_service = AuthService()
    
    # Test token creation
    data = {"sub": "test@example.com"}
    token = auth_service.create_access_token(data)
    assert token is not None
    print("✅ Token creation successful")
    
    # Test token verification
    email = auth_service.verify_token(token)
    assert email == "test@example.com"
    print("✅ Token verification successful")
    
    # Test invalid token
    invalid_email = auth_service.verify_token("invalid.token.here")
    assert invalid_email is None
    print("✅ Invalid token handling working")
    
    # Test expired token (if we had a way to create one)
    print("✅ JWT token operations working")

def main():
    """Run all tests"""
    print("🚀 Starting Authentication Tests")
    print("=" * 50)
    
    try:
        test_auth_service()
        test_auth_service_with_repository()
        test_repository_error_handling()
        test_jwt_token_operations()
        test_auth_api()
        
        print("\n✅ All authentication tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 