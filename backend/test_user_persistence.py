#!/usr/bin/env python3
"""
Test script to verify user persistence in database
Run this after starting the server: python -m uvicorn app.main:app --reload
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:8000"

def test_user_registration():
    """Test user registration"""
    print("🧪 Testing user registration...")
    
    # Test data
    user_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "SecurePass123"
    }
    
    try:
        # Register user
        response = requests.post(
            f"{BASE_URL}/auth/register",
            headers={"Content-Type": "application/json"},
            json=user_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ User registration successful!")
            return response.json()
        else:
            print("❌ User registration failed!")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the server is running:")
        print("   python -m uvicorn app.main:app --reload")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_user_login(email, password):
    """Test user login"""
    print(f"\n🧪 Testing user login for {email}...")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        # Login user
        response = requests.post(
            f"{BASE_URL}/auth/login",
            headers={"Content-Type": "application/json"},
            json=login_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ User login successful!")
            return response.json()
        else:
            print("❌ User login failed!")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_user_info(token):
    """Test getting user info with token"""
    print(f"\n🧪 Testing get user info...")
    
    try:
        # Get user info
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Get user info successful!")
            return response.json()
        else:
            print("❌ Get user info failed!")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 Testing User Persistence in Database")
    print("=" * 50)
    
    # Step 1: Register user
    user = test_user_registration()
    if not user:
        print("❌ Cannot proceed without user registration")
        return
    
    # Step 2: Login user
    login_result = test_user_login("testuser@example.com", "SecurePass123")
    if not login_result:
        print("❌ Cannot proceed without user login")
        return
    
    # Extract token
    token = login_result.get("access_token")
    if not token:
        print("❌ No access token received")
        return
    
    print(f"🔑 Token received: {token[:20]}...")
    
    # Step 3: Get user info
    user_info = test_get_user_info(token)
    if user_info:
        print("✅ User persistence test completed successfully!")
        print(f"📧 User email: {user_info.get('email')}")
        print(f"👤 User name: {user_info.get('full_name')}")
    else:
        print("❌ User persistence test failed!")

if __name__ == "__main__":
    main() 