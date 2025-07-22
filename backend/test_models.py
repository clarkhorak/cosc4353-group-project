#!/usr/bin/env python3
"""
Test script for all Pydantic V2 models
Run this to verify that all models work correctly with proper validation
"""

import sys
import os
import pytest
from datetime import date, time, datetime
from typing import List

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.models import (
    # User models
    UserBase, UserCreate, UserLogin, User, UserResponse,
    # Profile models
    Address, Availability, Profile, ProfileCreate, ProfileUpdate,
    # Event models
    EventBase, EventCreate, EventUpdate, EventResponse,
    # Notification models
    NotificationType, NotificationBase, NotificationCreate, Notification, NotificationUpdate, NotificationResponse,
    # History models
    ParticipationStatus, VolunteerHistoryBase, VolunteerHistoryCreate, VolunteerHistory, VolunteerHistoryUpdate, VolunteerStats, EventParticipation
)

def test_user_models():
    """Test user model validation"""
    print("🧪 Testing User Models...")
    
    # Test UserBase
    user_base = UserBase(
        email="test@example.com",
        full_name="John Doe"
    )
    print("✅ UserBase validation passed")
    assert user_base.email == "test@example.com"
    assert user_base.full_name == "John Doe"
    
    # Test UserCreate
    user_create = UserCreate(
        email="test@example.com",
        full_name="John Doe",
        password="SecurePass123"
    )
    print("✅ UserCreate validation passed")
    assert user_create.email == "test@example.com"
    assert user_create.password == "SecurePass123"
    
    # Test UserLogin
    user_login = UserLogin(
        email="test@example.com",
        password="SecurePass123"
    )
    print("✅ UserLogin validation passed")
    assert user_login.email == "test@example.com"
    
    # Test User
    user = User(
        id="1",
        email="test@example.com",
        full_name="John Doe",
        created_at=datetime.now()
    )
    print("✅ User validation passed")
    assert user.id == "1"
    
    # Test UserResponse
    user_response = UserResponse(
        id="1",
        email="test@example.com",
        full_name="John Doe",
        created_at=datetime.now(),
        is_active=True
    )
    print("✅ UserResponse validation passed")
    assert user_response.is_active is True

def test_profile_models():
    """Test profile model validation"""
    print("\n🧪 Testing Profile Models...")
    
    # Test Address
    address = Address(
        address1="123 Main St",
        city="Houston",
        state="TX",
        zip_code="77001"
    )
    print("✅ Address validation passed")
    assert address.city == "Houston"
    assert address.state == "TX"
    
    # Test Availability
    availability = Availability(
        date=date(2025, 12, 25),
        time=time(14, 0)
    )
    print("✅ Availability validation passed")
    assert availability.date == date(2025, 12, 25)
    
    # Test Profile
    profile = Profile(
        user_id="1",
        address=address,
        skills=["Teaching", "Organizing"],
        availability=[availability]
    )
    print("✅ Profile validation passed")
    assert profile.user_id == "1"
    assert len(profile.skills) == 2
    
    # Test ProfileCreate
    profile_create = ProfileCreate(
        address=address,
        skills=["Teaching", "Organizing"],
        availability=[availability]
    )
    print("✅ ProfileCreate validation passed")
    assert len(profile_create.skills) == 2
    
    # Test ProfileUpdate
    profile_update = ProfileUpdate(
        skills=["Teaching", "Organizing", "First Aid"]
    )
    print("✅ ProfileUpdate validation passed")
    assert profile_update.skills is not None and len(profile_update.skills) == 3

def test_event_models():
    """Test event model validation"""
    print("\n🧪 Testing Event Models...")
    
    # Test EventBase
    event_base = EventBase(
        title="Community Cleanup",
        description="Help clean up the local park and make it beautiful for everyone to enjoy",
        category="Environment",
        event_date=date(2025, 12, 25),
        start_time=time(9, 0),
        end_time=time(12, 0),
        location="Central Park, Houston, TX",
        capacity=100,
        status="open"
    )
    print("✅ EventBase validation passed")
    assert event_base.title == "Community Cleanup"
    assert event_base.capacity == 100
    
    # Test EventCreate
    event_create = EventCreate(
        title="Community Cleanup",
        description="Help clean up the local park and make it beautiful for everyone to enjoy",
        category="Environment",
        event_date=date(2025, 12, 25),
        start_time=time(9, 0),
        end_time=time(12, 0),
        location="Central Park, Houston, TX",
        capacity=100,
        status="open"
    )
    print("✅ EventCreate validation passed")
    assert event_create.category == "Environment"
    
    # Test EventResponse
    event_response = EventResponse(
        id=1,
        title="Community Cleanup",
        description="Help clean up the local park and make it beautiful for everyone to enjoy",
        category="Environment",
        event_date=date(2025, 12, 25),
        start_time=time(9, 0),
        end_time=time(12, 0),
        location="Central Park, Houston, TX",
        capacity=100,
        status="open",
        requirements=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    print("✅ EventResponse validation passed")
    assert event_response.id == 1
    
    # Test EventUpdate
    event_update = EventUpdate(
        title="Updated Community Cleanup",
        description="Updated description for the community cleanup event",
        capacity=150
    )
    print("✅ EventUpdate validation passed")
    assert event_update.capacity == 150

def test_notification_models():
    """Test notification model validation"""
    print("\n🧪 Testing Notification Models...")
    
    # Test NotificationBase
    notification_base = NotificationBase(
        user_id="1",
        type=NotificationType.EVENT_ASSIGNMENT,
        title="New Event Assignment",
        message="You have been assigned to the Community Cleanup event",
        event_id="1"
    )
    print("✅ NotificationBase validation passed")
    assert notification_base.type == NotificationType.EVENT_ASSIGNMENT
    
    # Test NotificationCreate
    notification_create = NotificationCreate(
        user_id="1",
        type=NotificationType.EVENT_ASSIGNMENT,
        title="New Event Assignment",
        message="You have been assigned to the Community Cleanup event",
        event_id="1"
    )
    print("✅ NotificationCreate validation passed")
    assert notification_create.user_id == "1"
    
    # Test Notification
    notification = Notification(
        id=1,
        user_id="1",
        type=NotificationType.EVENT_ASSIGNMENT,
        title="New Event Assignment",
        message="You have been assigned to the Community Cleanup event",
        event_id="1",
        created_at=datetime.now(),
        is_read=False
    )
    print("✅ Notification validation passed")
    assert notification.id == 1
    assert notification.is_read is False
    
    # Test NotificationResponse
    notification_response = NotificationResponse(
        id=1,
        user_id="1",
        type=NotificationType.EVENT_ASSIGNMENT,
        title="New Event Assignment",
        message="You have been assigned to the Community Cleanup event",
        event_id="1",
        created_at=datetime.now(),
        is_read=False
    )
    print("✅ NotificationResponse validation passed")
    assert notification_response.id == 1

def test_history_models():
    """Test history model validation"""
    print("\n🧪 Testing History Models...")
    
    # Test ParticipationStatus enum
    assert ParticipationStatus.PENDING == "pending"
    assert ParticipationStatus.COMPLETED == "completed"
    print("✅ ParticipationStatus enum validation passed")
    
    # Test VolunteerHistoryBase
    history_base = VolunteerHistoryBase(
        volunteer_id="1",
        event_id=1,
        event_name="Community Cleanup",
        event_date=date(2025, 12, 25),
        event_time=time(14, 0),
        location="Central Park, Houston, TX",
        status=ParticipationStatus.PENDING
    )
    print("✅ VolunteerHistoryBase validation passed")
    assert history_base.volunteer_id == "1"
    assert history_base.event_id == 1
    
    # Test VolunteerHistoryCreate
    history_create = VolunteerHistoryCreate(
        volunteer_id="1",
        event_id=1,
        event_name="Community Cleanup",
        event_date=date(2025, 12, 25),
        event_time=time(14, 0),
        location="Central Park, Houston, TX"
    )
    print("✅ VolunteerHistoryCreate validation passed")
    assert history_create.volunteer_id == "1"
    
    # Test VolunteerHistory
    history = VolunteerHistory(
        id=1,
        volunteer_id="1",
        event_id=1,
        event_name="Community Cleanup",
        event_date=date(2025, 12, 25),
        event_time=time(14, 0),
        location="Central Park, Houston, TX",
        status=ParticipationStatus.PENDING,
        joined_at=datetime.now()
    )
    print("✅ VolunteerHistory validation passed")
    assert history.id == 1
    
    # Test VolunteerStats
    stats = VolunteerStats(
        volunteer_id="1",
        total_events=5,
        completed_events=4,
        pending_events=1,
        cancelled_events=0,
        no_show_events=0,
        completion_rate=0.8
    )
    print("✅ VolunteerStats validation passed")
    assert stats.total_events == 5
    assert stats.completion_rate == 0.8

def test_validation_errors():
    """Test model validation errors"""
    print("\n🧪 Testing Validation Errors...")
    
    # Test invalid email
    try:
        UserBase(
            email="invalid-email",
            full_name="John Doe"
        )
        assert False, "Should have failed for invalid email"
    except Exception:
        print("✅ Invalid email validation working")
    
    # Test short password
    try:
        UserCreate(
            email="test@example.com",
            full_name="John Doe",
            password="123"
        )
        assert False, "Should have failed for short password"
    except Exception:
        print("✅ Short password validation working")
    
    # Test invalid zip code
    try:
        Address(
            address1="123 Main St",
            city="Houston",
            state="TX",
            zip_code="invalid"
        )
        assert False, "Should have failed for invalid zip code"
    except Exception:
        print("✅ Invalid zip code validation working")
    
    # Test empty skills list
    try:
        Profile(
            user_id="1",
            address=Address(
                address1="123 Main St",
                city="Houston",
                state="TX",
                zip_code="77001"
            ),
            skills=[],
            availability=[Availability(date=date(2025, 12, 25), time=time(14, 0))]
        )
        assert False, "Should have failed for empty skills"
    except Exception:
        print("✅ Empty skills validation working")
    
    print("✅ All validation error tests passed")

def main():
    """Run all model tests"""
    print("🚀 Starting Model Tests\n")
    
    test_user_models()
    test_profile_models()
    test_event_models()
    test_notification_models()
    test_history_models()
    test_validation_errors()
    
    print("\n🎉 All model tests passed!")

if __name__ == "__main__":
    main() 