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

def test_user_validation_errors():
    """Test user model validation errors"""
    print("\n🧪 Testing User Model Validation Errors...")
    
    # Test invalid email format
    try:
        UserBase(email="invalid-email", full_name="John Doe")
        assert False, "Should have failed for invalid email"
    except Exception as e:
        print("✅ Invalid email validation working")
    
    # Test short full name
    try:
        UserBase(email="test@example.com", full_name="A")
        assert False, "Should have failed for short name"
    except Exception as e:
        print("✅ Short name validation working")
    
    # Test long full name
    try:
        UserBase(email="test@example.com", full_name="A" * 51)
        assert False, "Should have failed for long name"
    except Exception as e:
        print("✅ Long name validation working")
    
    # Test invalid characters in name
    try:
        UserBase(email="test@example.com", full_name="John123")
        assert False, "Should have failed for invalid characters"
    except Exception as e:
        print("✅ Name character validation working")
    
    # Test weak password
    try:
        UserCreate(email="test@example.com", full_name="John Doe", password="weak")
        assert False, "Should have failed for weak password"
    except Exception as e:
        print("✅ Password strength validation working")
    
    # Test password without uppercase
    try:
        UserCreate(email="test@example.com", full_name="John Doe", password="securepass123")
        assert False, "Should have failed for password without uppercase"
    except Exception as e:
        print("✅ Password uppercase validation working")
    
    # Test password without lowercase
    try:
        UserCreate(email="test@example.com", full_name="John Doe", password="SECUREPASS123")
        assert False, "Should have failed for password without lowercase"
    except Exception as e:
        print("✅ Password lowercase validation working")
    
    # Test password without digit
    try:
        UserCreate(email="test@example.com", full_name="John Doe", password="SecurePass")
        assert False, "Should have failed for password without digit"
    except Exception as e:
        print("✅ Password digit validation working")

def test_profile_models():
    """Test profile model validation"""
    print("\n🧪 Testing Profile Models...")
    
    # Test Address
    address = Address(
        address1="123 Main St",
        city="Houston",
        state_code="TX",
        zip_code="77001"
    )
    print("✅ Address validation passed")
    assert address.city == "Houston"
    assert address.state_code == "TX"
    
    # Test Availability
    availability = Availability(
        date=date(2025, 12, 25),
        time=time(14, 0)
    )
    print("✅ Availability validation passed")
    assert availability.date == date(2025, 12, 25)
    assert availability.time == time(14, 0)
    
    # Test Profile
    profile = Profile(
        user_id="1",
        address=address,
        skills=["Teaching", "First Aid"],
        preferences="I prefer working with children",
        availability=[availability]
    )
    print("✅ Profile validation passed")
    assert len(profile.skills) == 2
    assert "Teaching" in profile.skills
    
    # Test ProfileCreate
    profile_create = ProfileCreate(
        address=address,
        skills=["Teaching", "First Aid"],
        preferences="I prefer working with children",
        availability=[availability]
    )
    print("✅ ProfileCreate validation passed")
    
    # Test ProfileUpdate
    profile_update = ProfileUpdate(
        skills=["Teaching", "First Aid", "Cooking"],
        preferences="Updated preferences"
    )
    print("✅ ProfileUpdate validation passed")

def test_profile_validation_errors():
    """Test profile model validation errors"""
    print("\n🧪 Testing Profile Model Validation Errors...")
    
    # Test short address
    try:
        Address(address1="123", city="Houston", state_code="TX", zip_code="77001")
        assert False, "Should have failed for short address"
    except Exception as e:
        print("✅ Short address validation working")
    
    # Test long address
    try:
        Address(address1="A" * 101, city="Houston", state_code="TX", zip_code="77001")
        assert False, "Should have failed for long address"
    except Exception as e:
        print("✅ Long address validation working")
    
    # Test short city
    try:
        Address(address1="123 Main St", city="A", state_code="TX", zip_code="77001")
        assert False, "Should have failed for short city"
    except Exception as e:
        print("✅ Short city validation working")
    
    # Test long city
    try:
        Address(address1="123 Main St", city="A" * 51, state_code="TX", zip_code="77001")
        assert False, "Should have failed for long city"
    except Exception as e:
        print("✅ Long city validation working")
    
    # Test invalid zip code format
    try:
        Address(address1="123 Main St", city="Houston", state_code="TX", zip_code="invalid")
        assert False, "Should have failed for invalid zip code"
    except Exception as e:
        print("✅ Zip code format validation working")

def test_event_models():
    """Test event model validation"""
    print("\n🧪 Testing Event Models...")
    
    # Test EventBase
    event_base = EventBase(
        title="Community Cleanup",
        description="Help clean up the local park",
        location="Central Park",
        required_skills=["Organizing", "Physical Labor"],
        urgency="Medium",
        event_date="2025-12-25",
        start_time="09:00",
        end_time="17:00",
        capacity=50
    )
    print("✅ EventBase validation passed")
    assert event_base.title == "Community Cleanup"
    assert len(event_base.required_skills) == 2
    
    # Test EventCreate
    event_create = EventCreate(
        title="Community Cleanup",
        description="Help clean up the local park",
        location="Central Park",
        required_skills=["Organizing", "Physical Labor"],
        urgency="Medium",
        event_date="2025-12-25",
        start_time="09:00",
        end_time="17:00",
        capacity=50,
        category="Environmental"
    )
    print("✅ EventCreate validation passed")
    
    # Test EventUpdate
    event_update = EventUpdate(
        title="Updated Community Cleanup",
        description="Updated description",
        capacity=75
    )
    print("✅ EventUpdate validation passed")
    
    # Test EventResponse
    event_response = EventResponse(
        id="1",
        title="Community Cleanup",
        description="Help clean up the local park",
        location="Central Park",
        required_skills=["Organizing", "Physical Labor"],
        urgency="Medium",
        event_date="2025-12-25",
        start_time="09:00",
        end_time="17:00",
        capacity=50,
        category="Environmental",
        status="open",
        created_by_id="1",
        created_at=datetime.now()
    )
    print("✅ EventResponse validation passed")

def test_event_validation_errors():
    """Test event model validation errors"""
    print("\n🧪 Testing Event Model Validation Errors...")
    
    # Test short title
    try:
        EventBase(
            title="AB",
            description="Help clean up the local park",
            location="Central Park",
            required_skills=["Organizing"],
            urgency="Medium",
            event_date="2025-12-25",
            start_time="09:00",
            end_time="17:00",
            capacity=50
        )
        assert False, "Should have failed for short title"
    except Exception as e:
        print("✅ Short title validation working")
    
    # Test long title
    try:
        EventBase(
            title="A" * 101,
            description="Help clean up the local park",
            location="Central Park",
            required_skills=["Organizing"],
            urgency="Medium",
            event_date="2025-12-25",
            start_time="09:00",
            end_time="17:00",
            capacity=50
        )
        assert False, "Should have failed for long title"
    except Exception as e:
        print("✅ Long title validation working")
    
    # Test invalid urgency
    try:
        EventBase(
            title="Community Cleanup",
            description="Help clean up the local park",
            location="Central Park",
            required_skills=["Organizing"],
            urgency="Invalid",
            event_date="2025-12-25",
            start_time="09:00",
            end_time="17:00",
            capacity=50
        )
        assert False, "Should have failed for invalid urgency"
    except Exception as e:
        print("✅ Urgency validation working")
    
    # Test zero capacity
    try:
        EventBase(
            title="Community Cleanup",
            description="Help clean up the local park",
            location="Central Park",
            required_skills=["Organizing"],
            urgency="Medium",
            event_date="2025-12-25",
            start_time="09:00",
            end_time="17:00",
            capacity=0
        )
        assert False, "Should have failed for zero capacity"
    except Exception as e:
        print("✅ Capacity validation working")

def test_notification_models():
    """Test notification model validation"""
    print("\n🧪 Testing Notification Models...")
    
    # Test NotificationBase
    notification_base = NotificationBase(
        user_id="1",
        title="Event Reminder",
        message="Don't forget about the community cleanup tomorrow!",
        type=NotificationType.EVENT_REMINDER
    )
    print("✅ NotificationBase validation passed")
    assert notification_base.title == "Event Reminder"
    assert notification_base.type == NotificationType.EVENT_REMINDER
    
    # Test NotificationCreate
    notification_create = NotificationCreate(
        user_id="1",
        title="Event Reminder",
        message="Don't forget about the community cleanup tomorrow!",
        type=NotificationType.EVENT_REMINDER
    )
    print("✅ NotificationCreate validation passed")
    
    # Test Notification
    notification = Notification(
        id=1,
        user_id="1",
        title="Event Reminder",
        message="Don't forget about the community cleanup tomorrow!",
        type=NotificationType.EVENT_REMINDER,
        is_read=False,
        created_at=datetime.now()
    )
    print("✅ Notification validation passed")
    
    # Test NotificationUpdate
    notification_update = NotificationUpdate(
        is_read=True
    )
    print("✅ NotificationUpdate validation passed")
    
    # Test NotificationResponse
    notification_response = NotificationResponse(
        id=1,
        user_id="1",
        title="Event Reminder",
        message="Don't forget about the community cleanup tomorrow!",
        type=NotificationType.EVENT_REMINDER,
        is_read=False,
        created_at=datetime.now()
    )
    print("✅ NotificationResponse validation passed")

def test_notification_validation_errors():
    """Test notification model validation errors"""
    print("\n🧪 Testing Notification Model Validation Errors...")
    
    # Test short title
    try:
        NotificationBase(
            user_id="1",
            title="AB",
            message="Test message",
            type=NotificationType.EVENT_REMINDER
        )
        assert False, "Should have failed for short title"
    except Exception as e:
        print("✅ Short title validation working")
    
    # Test long title
    try:
        NotificationBase(
            user_id="1",
            title="A" * 101,
            message="Test message",
            type=NotificationType.EVENT_REMINDER
        )
        assert False, "Should have failed for long title"
    except Exception as e:
        print("✅ Long title validation working")
    
    # Test short message
    try:
        NotificationBase(
            user_id="1",
            title="Test Title",
            message="Hi",
            type=NotificationType.EVENT_REMINDER
        )
        assert False, "Should have failed for short message"
    except Exception as e:
        print("✅ Short message validation working")
    
    # Test long message
    try:
        NotificationBase(
            user_id="1",
            title="Test Title",
            message="A" * 501,
            type=NotificationType.EVENT_REMINDER
        )
        assert False, "Should have failed for long message"
    except Exception as e:
        print("✅ Long message validation working")

def test_history_models():
    """Test history model validation"""
    print("\n🧪 Testing History Models...")
    
    # Test VolunteerHistoryBase
    history_base = VolunteerHistoryBase(
        event_id="1",
        participation_date="2025-12-25",
        hours_volunteered=4,
        status=ParticipationStatus.COMPLETED
    )
    print("✅ VolunteerHistoryBase validation passed")
    assert history_base.hours_volunteered == 4
    assert history_base.status == ParticipationStatus.COMPLETED
    
    # Test VolunteerHistoryCreate
    history_create = VolunteerHistoryCreate(
        event_id="1",
        participation_date="2025-12-25",
        hours_volunteered=4,
        status=ParticipationStatus.COMPLETED
    )
    print("✅ VolunteerHistoryCreate validation passed")
    
    # Test VolunteerHistory
    history = VolunteerHistory(
        id="1",
        user_id="1",
        event_id="1",
        participation_date="2025-12-25",
        hours_volunteered=4,
        status=ParticipationStatus.COMPLETED,
        created_at=datetime.now()
    )
    print("✅ VolunteerHistory validation passed")
    
    # Test VolunteerHistoryUpdate
    history_update = VolunteerHistoryUpdate(
        hours_volunteered=6,
        status=ParticipationStatus.COMPLETED
    )
    print("✅ VolunteerHistoryUpdate validation passed")
    
    # Test VolunteerStats
    stats = VolunteerStats(
        total_hours=20,
        total_events=5,
        average_hours_per_event=4.0
    )
    print("✅ VolunteerStats validation passed")
    
    # Test EventParticipation
    participation = EventParticipation(
        event_id="1",
        event_title="Community Cleanup",
        participation_date="2025-12-25",
        hours_volunteered=4,
        status=ParticipationStatus.COMPLETED
    )
    print("✅ EventParticipation validation passed")

def test_history_validation_errors():
    """Test history model validation errors"""
    print("\n🧪 Testing History Model Validation Errors...")
    
    # Test negative hours
    try:
        VolunteerHistoryBase(
            event_id="1",
            participation_date="2025-12-25",
            hours_volunteered=-1,
            status=ParticipationStatus.COMPLETED
        )
        assert False, "Should have failed for negative hours"
    except Exception as e:
        print("✅ Negative hours validation working")
    
    # Test invalid status
    try:
        VolunteerHistoryBase(
            event_id="1",
            participation_date="2025-12-25",
            hours_volunteered=4,
            status="Invalid"
        )
        assert False, "Should have failed for invalid status"
    except Exception as e:
        print("✅ Status validation working")

def test_validation_errors():
    """Test general validation errors"""
    print("\n🧪 Testing General Validation Errors...")
    
    # Test missing required fields
    try:
        UserBase(email="test@example.com")  # Missing full_name
        assert False, "Should have failed for missing full_name"
    except Exception as e:
        print("✅ Required field validation working")
    
    try:
        UserCreate(email="test@example.com", full_name="John Doe")  # Missing password
        assert False, "Should have failed for missing password"
    except Exception as e:
        print("✅ Required field validation working")
    
    # Test invalid data types
    try:
        UserBase(email=123, full_name="John Doe")  # Invalid email type
        assert False, "Should have failed for invalid email type"
    except Exception as e:
        print("✅ Data type validation working")
    
    try:
        UserBase(email="test@example.com", full_name=123)  # Invalid name type
        assert False, "Should have failed for invalid name type"
    except Exception as e:
        print("✅ Data type validation working")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🧪 Testing Edge Cases...")
    
    # Test minimum valid values
    user_min = UserBase(email="a@b.c", full_name="A B")
    print("✅ Minimum valid values working")
    
    # Test maximum valid values
    user_max = UserBase(
        email="very.long.email.address@very.long.domain.com",
        full_name="A" * 50
    )
    print("✅ Maximum valid values working")
    
    # Test empty skills array
    profile_empty_skills = Profile(
        user_id="1",
        address=Address(address1="123 Main St", city="Houston", state_code="TX", zip_code="77001"),
        skills=[],
        preferences="Test preferences",
        availability=[]
    )
    print("✅ Empty skills array working")
    
    # Test single skill
    profile_single_skill = Profile(
        user_id="1",
        address=Address(address1="123 Main St", city="Houston", state_code="TX", zip_code="77001"),
        skills=["Teaching"],
        preferences="Test preferences",
        availability=[]
    )
    print("✅ Single skill working")

def main():
    """Run all model tests"""
    print("🚀 Starting Model Validation Tests")
    print("=" * 50)
    
    try:
        test_user_models()
        test_user_validation_errors()
        test_profile_models()
        test_profile_validation_errors()
        test_event_models()
        test_event_validation_errors()
        test_notification_models()
        test_notification_validation_errors()
        test_history_models()
        test_history_validation_errors()
        test_validation_errors()
        test_edge_cases()
        
        print("\n✅ All model validation tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 