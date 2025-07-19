import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date, time
import uuid
from app.main import app

client = TestClient(app)

# Test data templates
def get_test_user_data():
    """Generate unique test user data"""
    unique_id = str(uuid.uuid4()).replace('-', '')[:8]
    return {
        "email": f"test{unique_id}@example.com",
        "full_name": f"Test User",
        "password": "SecurePass123"
    }

def get_test_profile_data():
    """Generate test profile data"""
    return {
        "address": {
            "address1": "123 Main St",
            "city": "Houston",
            "state": "TX",
            "zip_code": "77001"
        },
        "skills": ["Teaching", "Organizing"],
        "availability": [
            {
                "date": "2025-12-25",
                "time": "14:00:00"
            }
        ]
    }

def get_test_event_data():
    """Generate test event data"""
    return {
        "title": "Community Cleanup",
        "description": "Help clean up the local park",
        "category": "Environment",
        "event_date": "2025-12-25",
        "start_time": "09:00:00",
        "end_time": "12:00:00",
        "location": "Central Park, Houston, TX",
        "capacity": 100,
        "status": "open"
    }

@pytest.fixture
def auth_token():
    """Get authentication token for testing"""
    # Register user with unique data
    user_data = get_test_user_data()
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Get headers with authentication token"""
    return {"Authorization": f"Bearer {auth_token}"}

# Authentication API Tests
def test_auth_register_success():
    """Test successful user registration"""
    user_data = get_test_user_data()
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data

def test_auth_register_duplicate_email():
    """Test registration with duplicate email"""
    user_data = get_test_user_data()
    # First registration
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Second registration with same email
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_auth_register_invalid_email():
    """Test registration with invalid email"""
    user_data = get_test_user_data()
    user_data["email"] = "invalid-email"
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422

def test_auth_register_weak_password():
    """Test registration with weak password"""
    user_data = get_test_user_data()
    user_data["password"] = "123"
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422

def test_auth_login_success():
    """Test successful login"""
    user_data = get_test_user_data()
    # Register user first
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data

def test_auth_login_invalid_credentials():
    """Test login with invalid credentials"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401

def test_auth_me_success(auth_headers):
    """Test getting current user info"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data

def test_auth_me_invalid_token():
    """Test getting current user with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401

def test_auth_verify_token_success(auth_headers):
    """Test token verification"""
    response = client.get("/auth/verify-token", headers=auth_headers)
    assert response.status_code == 200

def test_auth_logout_success(auth_headers):
    """Test logout"""
    response = client.post("/auth/logout", headers=auth_headers)
    assert response.status_code == 200

# Profile API Tests
def test_profile_create_success(auth_headers):
    """Test successful profile creation"""
    profile_data = get_test_profile_data()
    response = client.post("/profile", json=profile_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["skills"] == profile_data["skills"]

def test_profile_create_invalid_address(auth_headers):
    """Test profile creation with invalid address"""
    profile_data = get_test_profile_data()
    profile_data["address"]["zip_code"] = "invalid"
    response = client.post("/profile", json=profile_data, headers=auth_headers)
    assert response.status_code == 422

def test_profile_get_success(auth_headers):
    """Test getting user profile"""
    profile_data = get_test_profile_data()
    # Create profile first
    client.post("/profile", json=profile_data, headers=auth_headers)
    
    # Get profile
    response = client.get("/profile", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data

def test_profile_get_not_found(auth_headers):
    """Test getting profile when none exists"""
    response = client.get("/profile", headers=auth_headers)
    assert response.status_code == 404

def test_profile_update_success(auth_headers):
    """Test successful profile update"""
    profile_data = get_test_profile_data()
    # Create profile first
    client.post("/profile", json=profile_data, headers=auth_headers)
    
    # Update profile
    update_data = {"skills": ["Teaching", "First Aid"]}
    response = client.put("/profile", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["skills"] == ["Teaching", "First Aid"]

def test_profile_update_not_found(auth_headers):
    """Test updating profile when none exists"""
    update_data = {"skills": ["Teaching"]}
    response = client.put("/profile", json=update_data, headers=auth_headers)
    assert response.status_code == 404

def test_profile_delete_success(auth_headers):
    """Test successful profile deletion"""
    profile_data = get_test_profile_data()
    # Create profile first
    client.post("/profile", json=profile_data, headers=auth_headers)
    
    # Delete profile
    response = client.delete("/profile", headers=auth_headers)
    assert response.status_code == 200

def test_profile_delete_not_found(auth_headers):
    """Test deleting profile when none exists"""
    response = client.delete("/profile", headers=auth_headers)
    assert response.status_code == 404

# Event API Tests
def test_event_create_success(auth_headers):
    """Test successful event creation"""
    event_data = get_test_event_data()
    response = client.post("/events", json=event_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert "id" in data

def test_event_create_invalid_date(auth_headers):
    """Test event creation with past date"""
    event_data = get_test_event_data()
    event_data["event_date"] = "2020-01-01"
    response = client.post("/events", json=event_data, headers=auth_headers)
    assert response.status_code == 422

def test_event_list_success(auth_headers):
    """Test listing events"""
    event_data = get_test_event_data()
    # Create an event first
    client.post("/events", json=event_data, headers=auth_headers)
    
    # List events
    response = client.get("/events", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_event_get_by_id_success(auth_headers):
    """Test getting event by ID"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Get event by ID
    response = client.get(f"/events/{event_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id

def test_event_get_by_id_not_found(auth_headers):
    """Test getting non-existent event"""
    response = client.get("/events/999", headers=auth_headers)
    assert response.status_code == 404

def test_event_update_success(auth_headers):
    """Test successful event update"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Update event
    update_data = {"title": "Updated Event Title"}
    response = client.put(f"/events/{event_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Event Title"

def test_event_update_not_found(auth_headers):
    """Test updating non-existent event"""
    update_data = {"title": "Updated Title"}
    response = client.put("/events/999", json=update_data, headers=auth_headers)
    assert response.status_code == 404

def test_event_delete_success(auth_headers):
    """Test successful event deletion"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Delete event
    response = client.delete(f"/events/{event_id}", headers=auth_headers)
    assert response.status_code == 200

def test_event_delete_not_found(auth_headers):
    """Test deleting non-existent event"""
    response = client.delete("/events/999", headers=auth_headers)
    assert response.status_code == 404

# History API Tests
def test_history_participate_success(auth_headers):
    """Test successful event participation"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Participate in event
    response = client.post(f"/history/participate/{event_id}", headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["event_id"] == event_id

def test_history_participate_duplicate(auth_headers):
    """Test duplicate participation prevention"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Participate twice
    client.post(f"/history/participate/{event_id}", headers=auth_headers)
    response = client.post(f"/history/participate/{event_id}", headers=auth_headers)
    assert response.status_code == 400

def test_history_get_user_history(auth_headers):
    """Test getting user history"""
    event_data = get_test_event_data()
    # Create and participate in an event
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    client.post(f"/history/participate/{event_id}", headers=auth_headers)
    
    # Get history
    response = client.get("/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_history_get_stats(auth_headers):
    """Test getting user statistics"""
    event_data = get_test_event_data()
    # Create and participate in an event
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    client.post(f"/history/participate/{event_id}", headers=auth_headers)
    
    # Get stats
    response = client.get("/history/stats", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_events" in data
    assert "completion_rate" in data

# Matching API Tests
def test_matching_signup_success(auth_headers):
    """Test successful event signup"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Sign up for event
    response = client.post(f"/matching/signup/{event_id}", headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["event_id"] == event_id

def test_matching_signup_duplicate(auth_headers):
    """Test duplicate signup prevention"""
    event_data = get_test_event_data()
    # Create an event first
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    
    # Sign up twice
    client.post(f"/matching/signup/{event_id}", headers=auth_headers)
    response = client.post(f"/matching/signup/{event_id}", headers=auth_headers)
    assert response.status_code == 400

def test_matching_cancel_signup_success(auth_headers):
    """Test successful signup cancellation"""
    event_data = get_test_event_data()
    # Create an event and sign up
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    client.post(f"/matching/signup/{event_id}", headers=auth_headers)
    
    # Cancel signup
    response = client.delete(f"/matching/signup/{event_id}", headers=auth_headers)
    assert response.status_code == 200

def test_matching_list_event_signups(auth_headers):
    """Test listing signups for an event"""
    event_data = get_test_event_data()
    # Create an event and sign up
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    client.post(f"/matching/signup/{event_id}", headers=auth_headers)
    
    # List signups
    response = client.get(f"/matching/event/{event_id}/signups", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_matching_list_volunteer_signups(auth_headers):
    """Test listing signups for a volunteer"""
    event_data = get_test_event_data()
    # Create an event and sign up
    create_response = client.post("/events", json=event_data, headers=auth_headers)
    event_id = create_response.json()["id"]
    client.post(f"/matching/signup/{event_id}", headers=auth_headers)
    
    # List volunteer signups
    response = client.get("/matching/volunteer/signups", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Notification API Tests
def test_notification_create_success(auth_headers):
    """Test successful notification creation"""
    notification_data = {
        "type": "event_assignment",
        "title": "New Event Assignment",
        "message": "You have been assigned to an event",
        "event_id": "1"
    }
    response = client.post("/notifications", json=notification_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == notification_data["title"]

def test_notification_list_user_notifications(auth_headers):
    """Test listing user notifications"""
    # Create a notification first
    notification_data = {
        "type": "event_assignment",
        "title": "Test Notification",
        "message": "Test message",
        "event_id": "1"
    }
    client.post("/notifications", json=notification_data, headers=auth_headers)
    
    # List notifications
    response = client.get("/notifications", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_notification_mark_as_read(auth_headers):
    """Test marking notification as read"""
    # Create a notification first
    notification_data = {
        "type": "event_assignment",
        "title": "Test Notification",
        "message": "Test message",
        "event_id": "1"
    }
    create_response = client.post("/notifications", json=notification_data, headers=auth_headers)
    notification_id = create_response.json()["id"]
    
    # Mark as read
    response = client.put(f"/notifications/{notification_id}/read", headers=auth_headers)
    assert response.status_code == 200

def test_notification_delete_success(auth_headers):
    """Test successful notification deletion"""
    # Create a notification first
    notification_data = {
        "type": "event_assignment",
        "title": "Test Notification",
        "message": "Test message",
        "event_id": "1"
    }
    create_response = client.post("/notifications", json=notification_data, headers=auth_headers)
    notification_id = create_response.json()["id"]
    
    # Delete notification
    response = client.delete(f"/notifications/{notification_id}", headers=auth_headers)
    assert response.status_code == 200 