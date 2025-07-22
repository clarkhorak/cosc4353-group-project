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

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.auth_service import AuthService
from app.models.user import UserCreate, UserLogin

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
    
    response = requests.post(f"{base_url}/auth/register", json=register_data)
    assert response.status_code == 201, f"Registration API failed: {response.status_code} - {response.text}"
    print("✅ Registration API working")
    user_data = response.json()
    
    # Test login
    login_data = {
        "email": "apitest@example.com",
        "password": "SecurePass123"
    }
    
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    assert response.status_code == 200, f"Login API failed: {response.status_code} - {response.text}"
    print("✅ Login API working")
    token_data = response.json()
    access_token = token_data["access_token"]
    
    # Test get current user
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{base_url}/auth/me", headers=headers)
    assert response.status_code == 200, f"Get current user API failed: {response.status_code} - {response.text}"
    print("✅ Get current user API working")
    
    # Test token verification
    response = requests.get(f"{base_url}/auth/verify-token", headers=headers)
    assert response.status_code == 200, f"Token verification API failed: {response.status_code} - {response.text}"
    print("✅ Token verification API working")
    
    # Test invalid token
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{base_url}/auth/me", headers=invalid_headers)
    assert response.status_code == 401, f"Invalid token should have been rejected: {response.status_code}"
    print("✅ Invalid token validation working")
    
    # Test logout
    response = requests.post(f"{base_url}/auth/logout", headers=headers)
    assert response.status_code == 200, f"Logout API failed: {response.status_code} - {response.text}"
    print("✅ Logout API working")
    
    print("✅ All Auth API tests passed")

def main():
    """Run all authentication tests"""
    print("🚀 Starting Authentication Tests\n")
    
    # Test the service directly
    test_auth_service()
    
    # Test the API endpoints (only if server is running)
    try:
        test_auth_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Auth API test failed: {e}")

if __name__ == "__main__":
    main() 