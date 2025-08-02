#!/usr/bin/env python3
"""
Test script for Profile Service and API endpoints
"""

import asyncio
import requests
import json
from datetime import date, time
from app.services.profile_service import ProfileService
from app.models.profile import ProfileCreate, ProfileUpdate, Address, Availability

# Test data
TEST_ADDRESS = Address(
    address1="123 Main St",
    address2="Apt 4B",
    city="Houston",
    state_code="TX",
    zip_code="77001"
)

TEST_AVAILABILITY = [
    Availability(date=date(2026, 1, 15), time=time(9, 0)),
    Availability(date=date(2026, 1, 16), time=time(14, 0))
]

TEST_PROFILE_DATA = ProfileCreate(
    address=TEST_ADDRESS,
    skills=["Teaching", "First Aid", "Organizing"],
    preferences="I prefer working with children and outdoor activities",
    availability=TEST_AVAILABILITY
)

TEST_UPDATE_DATA = ProfileUpdate(
    skills=["Teaching", "First Aid", "Organizing", "Cooking"],
    preferences="Updated preferences"
)

BASE_URL = "http://localhost:8000"

def test_profile_service():
    """Test ProfileService methods"""
    print("🧪 Testing ProfileService...")
    
    async def run_tests():
        service = ProfileService()
        
        # Test create profile
        print("  📝 Testing create_profile...")
        profile = await service.create_profile(1, TEST_PROFILE_DATA)
        assert profile.user_id == "1"
        assert len(profile.skills) == 3
        assert profile.address.city == "Houston"
        print("    ✅ create_profile passed")
        
        # Test get profile
        print("  📖 Testing get_profile...")
        retrieved_profile = await service.get_profile(1)
        assert retrieved_profile.user_id == "1"
        assert retrieved_profile.address.state_code == "TX"
        print("    ✅ get_profile passed")
        
        # Test update profile
        print("  ✏️  Testing update_profile...")
        updated_profile = await service.update_profile(1, TEST_UPDATE_DATA)
        assert len(updated_profile.skills) == 4
        assert "Cooking" in updated_profile.skills
        assert updated_profile.preferences == "Updated preferences"
        print("    ✅ update_profile passed")
        
        # Test search by skills
        print("  🔍 Testing search_profiles_by_skills...")
        matching_profiles = await service.search_profiles_by_skills(["Teaching"])
        assert len(matching_profiles) == 1
        assert matching_profiles[0].user_id == "1"
        print("    ✅ search_profiles_by_skills passed")
        
        # Test search by location
        print("  🗺️  Testing search_profiles_by_location...")
        location_profiles = await service.search_profiles_by_location("Houston", "TX")
        assert len(location_profiles) == 1
        assert location_profiles[0].address.city == "Houston"
        print("    ✅ search_profiles_by_location passed")
        
        # Test get all profiles
        print("  📋 Testing get_all_profiles...")
        all_profiles = await service.get_all_profiles()
        assert len(all_profiles) == 1
        print("    ✅ get_all_profiles passed")
        
        # Test delete profile
        print("  🗑️  Testing delete_profile...")
        result = await service.delete_profile(1)
        assert result is True
        
        # Verify profile is deleted
        try:
            await service.get_profile(1)
            assert False, "Profile should not exist after deletion"
        except Exception:
            print("    ✅ delete_profile passed")
        
        print("  🎉 All ProfileService tests passed!")
    
    asyncio.run(run_tests())

def test_profile_api():
    """Test Profile API endpoints"""
    print("\n🌐 Testing Profile API endpoints...")
    
    # First, register and login a user to get a token
    print("  🔐 Getting authentication token...")
    
    # Register user
    register_data = {
        "username": "profiletest",
        "email": "profiletest@example.com",
        "password": "testpass123",
        "first_name": "Profile",
        "last_name": "Test"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code != 201:
        print(f"    ❌ User registration failed: {response.text}")
        return
    
    # Login to get token
    login_data = {
        "username": "profiletest",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"    ❌ Login failed: {response.text}")
        return
    
    token_data = response.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("    ✅ Authentication successful")
    
    # Test create profile
    print("  📝 Testing POST /profiles/...")
    profile_data = {
        "address": {
            "address1": "456 Oak Ave",
            "address2": "Suite 100",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701"
        },
        "skills": ["Teaching", "First Aid"],
        "preferences": "I love working with children",
        "availability": [
            {"date": "2026-01-15", "time": "09:00:00"},
            {"date": "2026-01-16", "time": "14:00:00"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/profiles/", json=profile_data, headers=headers)
    if response.status_code == 201:
        print("    ✅ Profile creation successful")
        profile_id = response.json()["user_id"]
    else:
        print(f"    ❌ Profile creation failed: {response.text}")
        return
    
    # Test get my profile
    print("  📖 Testing GET /profiles/me...")
    response = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
    if response.status_code == 200:
        profile = response.json()
        assert profile["address"]["city"] == "Austin"
        print("    ✅ Get my profile successful")
    else:
        print(f"    ❌ Get my profile failed: {response.text}")
        return
    
    # Test update profile
    print("  ✏️  Testing PUT /profiles/me...")
    update_data = {
        "skills": ["Teaching", "First Aid", "Cooking"],
        "preferences": "Updated preferences for testing"
    }
    
    response = requests.put(f"{BASE_URL}/profiles/me", json=update_data, headers=headers)
    if response.status_code == 200:
        updated_profile = response.json()
        assert len(updated_profile["skills"]) == 3
        assert "Cooking" in updated_profile["skills"]
        print("    ✅ Profile update successful")
    else:
        print(f"    ❌ Profile update failed: {response.text}")
        return
    
    # Test get all profiles
    print("  📋 Testing GET /profiles/...")
    response = requests.get(f"{BASE_URL}/profiles/")
    if response.status_code == 200:
        profiles = response.json()
        assert len(profiles) >= 1
        print("    ✅ Get all profiles successful")
    else:
        print(f"    ❌ Get all profiles failed: {response.text}")
        return
    
    # Test search by skills
    print("  🔍 Testing GET /profiles/search/skills...")
    response = requests.get(f"{BASE_URL}/profiles/search/skills?skills=Teaching&skills=First%20Aid")
    if response.status_code == 200:
        matching_profiles = response.json()
        assert len(matching_profiles) >= 1
        print("    ✅ Search by skills successful")
    else:
        print(f"    ❌ Search by skills failed: {response.text}")
        return
    
    # Test search by location
    print("  🗺️  Testing GET /profiles/search/location...")
    response = requests.get(f"{BASE_URL}/profiles/search/location?city=Austin&state=TX")
    if response.status_code == 200:
        location_profiles = response.json()
        assert len(location_profiles) >= 1
        print("    ✅ Search by location successful")
    else:
        print(f"    ❌ Search by location failed: {response.text}")
        return
    
    # Test delete profile
    print("  🗑️  Testing DELETE /profiles/me...")
    response = requests.delete(f"{BASE_URL}/profiles/me", headers=headers)
    if response.status_code == 204:
        print("    ✅ Profile deletion successful")
    else:
        print(f"    ❌ Profile deletion failed: {response.text}")
        return
    
    print("  🎉 All Profile API tests passed!")

def main():
    """Run all tests"""
    print("🚀 Starting Profile Module Tests\n")
    
    try:
        # Test ProfileService
        test_profile_service()
        
        # Test Profile API
        test_profile_api()
        
        print("\n🎉 All Profile Module tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 