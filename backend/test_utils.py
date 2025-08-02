#!/usr/bin/env python3
"""
Test utilities for database seeding and cleanup
"""

import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import get_db
from app.models.database import User, Profile, Event, History, Notification, State
from app.services.auth_service import AuthService

def create_test_user(session: Session, user_id: str = "user1", email: str = "test@example.com") -> User:
    """Create a test user in the database"""
    # Clean up any existing test user to ensure fresh hash
    existing_user = session.query(User).filter(User.email == email).first()
    if existing_user:
        print(f"🗑️ Cleaning up existing test user: {existing_user.email}")
        session.delete(existing_user)
        session.commit()
    
    # Create new user with properly hashed password
    auth_service = AuthService()
    hashed_password = auth_service.hash_password("TestPassword123")
    
    user = User(
        id=user_id,
        email=email,
        full_name="Test User",
        hashed_password=hashed_password,
        is_active=True,
        created_at=datetime.now()
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    print(f"✅ Created fresh test user with hash: {hashed_password[:20]}...")
    return user

def create_test_state(session: Session, state_code: str = "TX", state_name: str = "Texas") -> State:
    """Create a test state in the database"""
    # Check if state already exists
    existing_state = session.query(State).filter(State.code == state_code).first()
    if existing_state:
        return existing_state
    
    state = State(
        code=state_code,
        name=state_name,
        created_at=datetime.now()
    )
    
    session.add(state)
    session.commit()
    session.refresh(state)
    return state

def create_test_event(session: Session, event_id: str = "event1", created_by_id: str = "user1") -> Event:
    """Create a test event in the database"""
    # Check if event already exists
    existing_event = session.query(Event).filter(Event.id == event_id).first()
    if existing_event:
        return existing_event
    
    event = Event(
        id=event_id,
        title="Test Community Cleanup",
        description="A test event for cleaning up the community",
        location="Test Park",
        requirements="No special requirements",
        required_skills="Teaching,Organizing",
        category="Environmental",
        urgency="Medium",
        event_date="2025-12-25",
        start_time="09:00",
        end_time="17:00",
        capacity=50,
        status="open",
        created_by_id=created_by_id,
        created_at=datetime.now()
    )
    
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

def create_test_profile(session: Session, user_id: str = "user1") -> Profile:
    """Create a test profile in the database"""
    # Check if profile already exists
    existing_profile = session.query(Profile).filter(Profile.user_id == user_id).first()
    if existing_profile:
        return existing_profile
    
    # Ensure state exists before creating profile
    create_test_state(session, "TX", "Texas")
    
    profile = Profile(
        user_id=user_id,
        address1="123 Test Street",
        city="Test City",
        state_code="TX",
        zip_code="77001",
        skills="Teaching,First Aid",
        availability="[{\"date\": \"2025-12-25\", \"time\": \"09:00:00\"}]",
        preferences="I prefer working with children",
        created_at=datetime.now()
    )
    
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

def create_test_history(session: Session, user_id: str = "user1", event_id: str = "event1") -> History:
    """Create a test history record in the database"""
    # Check if history already exists
    existing_history = session.query(History).filter(
        History.user_id == user_id,
        History.event_id == event_id
    ).first()
    if existing_history:
        return existing_history
    
    history = History(
        user_id=user_id,
        event_id=event_id,
        participation_date="2025-12-25",
        hours_volunteered=4,
        status="completed",
        created_at=datetime.now()
    )
    
    session.add(history)
    session.commit()
    session.refresh(history)
    return history

def create_test_notification(session: Session, user_id: str = "user1") -> Notification:
    """Create a test notification in the database"""
    notification = Notification(
        user_id=user_id,
        title="Test Notification",
        message="This is a test notification message",
        type="info",
        is_read=False,
        created_at=datetime.now()
    )
    
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification

def cleanup_all_test_data_safe(session: Session):
    """Clean up ALL test data from the database with safe deletion order"""
    print("🧹 Cleaning up all test data (safe mode)...")
    
    try:
        # Delete in proper order to respect foreign key constraints
        # Child tables first, then parent tables
        
        # 1. Notifications (child of users)
        notifications_deleted = session.query(Notification).filter(Notification.user_id == "user1").delete()
        print(f"✅ Deleted {notifications_deleted} notifications")
        
        # 2. History (child of both users and events)
        history_deleted = session.query(History).filter(History.user_id == "user1").delete()
        print(f"✅ Deleted {history_deleted} history records")
        
        # 3. Profiles (child of users)
        profiles_deleted = session.query(Profile).filter(Profile.user_id == "user1").delete()
        print(f"✅ Deleted {profiles_deleted} profiles")
        
        # 4. Events (child of users via created_by_id) - MUST be deleted before users
        events_deleted = session.query(Event).filter(Event.created_by_id == "user1").delete()
        print(f"✅ Deleted {events_deleted} events")
        
        # 5. Users (parent table) - now safe to delete
        users_deleted = session.query(User).filter(User.email == "test@example.com").delete()
        print(f"✅ Deleted {users_deleted} users")
        
        # Note: We don't delete the state as it might be used by other profiles
        session.commit()
        print("✅ All test data cleaned up safely")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        session.rollback()
        raise

def cleanup_all_test_data(session: Session):
    """Clean up ALL test data from the database to ensure fresh start"""
    print("🧹 Cleaning up all test data...")
    
    # Delete in proper order to respect foreign key constraints
    # Child tables first, then parent tables
    session.query(Notification).filter(Notification.user_id == "user1").delete()
    session.query(History).filter(History.user_id == "user1").delete()
    session.query(Profile).filter(Profile.user_id == "user1").delete()
    session.query(Event).filter(Event.id == "event1").delete()
    session.query(User).filter(User.email == "test@example.com").delete()
    # Note: We don't delete the state as it might be used by other profiles
    session.commit()
    print("✅ All test data cleaned up")

def get_test_session():
    """Get a test database session"""
    from app.database import get_session_local
    SessionLocal = get_session_local()
    return SessionLocal()

def setup_test_database():
    """Set up test database with all required test data"""
    session = get_test_session()
    try:
        # Clean up any existing test data first (using safe cleanup)
        cleanup_all_test_data_safe(session)
        
        # Create test user (this will create a fresh user with proper hash)
        user = create_test_user(session)
        print(f"✅ Created test user: {user.email}")
        
        # Create test event
        event = create_test_event(session, created_by_id=user.id)
        print(f"✅ Created test event: {event.title}")
        
        # Create test profile (this will also create the required state)
        profile = create_test_profile(session, user_id=user.id)
        print(f"✅ Created test profile for user: {user.id}")
        
        # Create test history
        history = create_test_history(session, user_id=user.id, event_id=event.id)
        print(f"✅ Created test history record")
        
        # Create test notification
        notification = create_test_notification(session, user_id=user.id)
        print(f"✅ Created test notification")
        
        return {
            "user": user,
            "event": event,
            "profile": profile,
            "history": history,
            "notification": notification
        }
        
    except Exception as e:
        print(f"❌ Error setting up test database: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def get_test_auth_token() -> str:
    """Get a valid auth token for testing"""
    auth_service = AuthService()
    
    # Create test user if it doesn't exist (this will clean up and recreate)
    session = get_test_session()
    try:
        # Clean up and create fresh user (using safe cleanup)
        cleanup_all_test_data_safe(session)
        user = create_test_user(session)
        
        print(f"✅ Created fresh user with ID: {user.id}")
        print(f"✅ User email: {user.email}")
        print(f"✅ User hashed password: {user.hashed_password[:20]}...")
        
        # Test password verification directly
        test_password = "TestPassword123"
        is_valid = auth_service.verify_password(test_password, user.hashed_password)
        print(f"✅ Password verification test: {is_valid}")
        
        if not is_valid:
            print("❌ Password verification failed - this is the root cause!")
            # Let's try to hash the password again and compare
            new_hash = auth_service.hash_password(test_password)
            print(f"✅ New hash: {new_hash[:20]}...")
            print(f"✅ Stored hash: {user.hashed_password[:20]}...")
            print(f"✅ Hashes match: {new_hash == user.hashed_password}")
            
            # Test with passlib directly
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            direct_hash = pwd_context.hash(test_password)
            direct_verify = pwd_context.verify(test_password, user.hashed_password)
            print(f"✅ Direct passlib hash: {direct_hash[:20]}...")
            print(f"✅ Direct passlib verification: {direct_verify}")
            
            # Test with bcrypt directly
            import bcrypt
            bcrypt_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
            bcrypt_verify = bcrypt.checkpw(test_password.encode('utf-8'), user.hashed_password.encode('utf-8'))
            print(f"✅ Direct bcrypt verification: {bcrypt_verify}")
            
            raise ValueError("Password verification failed even with fresh user")
        
        # Create login data with the same password used when creating the user
        from app.models.user import UserLogin
        login_data = UserLogin(
            email="test@example.com",
            password="TestPassword123"  # This should match the password used in create_test_user
        )
        
        # Get token
        token = auth_service.authenticate_user(login_data)
        if token:
            print(f"✅ Successfully generated auth token: {token[:50]}...")
            return token
        else:
            raise ValueError("Failed to authenticate test user - check password hashing")
        
    finally:
        session.close()

if __name__ == "__main__":
    print("🧪 Setting up test database...")
    test_data = setup_test_database()
    print("✅ Test database setup complete!")
    
    # Test auth token
    try:
        token = get_test_auth_token()
        if token:
            print(f"✅ Test auth token: {token[:50]}...")
        else:
            print("❌ Failed to generate auth token.")
    except Exception as e:
        print(f"❌ Error generating auth token: {e}") 