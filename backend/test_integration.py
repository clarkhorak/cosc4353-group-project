import pytest
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.database import get_database_url, get_engine
from app.models.database import Base, User
from app.services.auth_service import AuthService
from app.models.user import UserCreate

class TestDatabaseIntegration:
    """Test database integration and user persistence"""
    
    def setup_method(self):
        """Setup test environment"""
        # Get database URL
        self.database_url = get_database_url()
        self.engine = get_engine()
        
        # Create test session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)
    
    def teardown_method(self):
        """Cleanup test environment"""
        # Clean up test data
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()
    
    def test_database_connection(self):
        """Test that database connection works"""
        try:
            # Try to execute a simple query using text()
            result = self.session.execute(text("SELECT 1"))
            assert result is not None
            print("✅ Database connection successful")
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")
    
    def test_user_creation_in_database(self):
        """Test that user creation actually persists to database"""
        # Create test user data
        user_data = UserCreate(
            email="integration@test.com",
            full_name="Integration Test User",
            password="TestPassword123"
        )
        
        # Create auth service
        auth_service = AuthService()
        
        # Register user
        user = auth_service.register_user(user_data)
        
        # Verify user was created in database
        db_user = self.session.query(User).filter(User.email == "integration@test.com").first()
        assert db_user is not None
        assert db_user.email == "integration@test.com"
        assert db_user.full_name == "Integration Test User"
        assert db_user.is_active == True
        assert db_user.hashed_password is not None
        
        # Verify returned user object matches database
        assert user.id == db_user.id
        assert user.email == db_user.email
        assert user.full_name == db_user.full_name
        assert user.is_active == db_user.is_active
        
        print("✅ User creation in database successful")
    
    def test_user_authentication_from_database(self):
        """Test that user authentication works with database"""
        # Create test user data
        user_data = UserCreate(
            email="auth@test.com",
            full_name="Auth Test User",
            password="TestPassword123"
        )
        
        # Create auth service
        auth_service = AuthService()
        
        # Register user
        user = auth_service.register_user(user_data)
        
        # Create login data
        from app.models.user import UserLogin
        login_data = UserLogin(
            email="auth@test.com",
            password="TestPassword123"
        )
        
        # Authenticate user
        token = auth_service.authenticate_user(login_data)
        
        # Verify authentication succeeded
        assert token is not None
        
        # Verify token can be decoded
        decoded_email = auth_service.verify_token(token)
        assert decoded_email == "auth@test.com"
        
        print("✅ User authentication from database successful")
    
    def test_duplicate_user_registration_fails(self):
        """Test that duplicate user registration fails"""
        # Create test user data
        user_data = UserCreate(
            email="duplicate@test.com",
            full_name="Duplicate Test User",
            password="TestPassword123"
        )
        
        # Create auth service
        auth_service = AuthService()
        
        # Register user first time
        user1 = auth_service.register_user(user_data)
        assert user1 is not None
        
        # Try to register same user again
        with pytest.raises(ValueError, match="User with this email already exists"):
            auth_service.register_user(user_data)
        
        print("✅ Duplicate user registration prevention working")

def main():
    """Run integration tests"""
    print("🚀 Starting Database Integration Tests")
    print("=" * 50)
    
    # Create test instance
    test_instance = TestDatabaseIntegration()
    
    try:
        test_instance.setup_method()
        
        test_instance.test_database_connection()
        test_instance.test_user_creation_in_database()
        test_instance.test_user_authentication_from_database()
        test_instance.test_duplicate_user_registration_fails()
        
        test_instance.teardown_method()
        
        print("\n✅ All integration tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if hasattr(test_instance, 'session'):
            test_instance.session.close()

if __name__ == "__main__":
    main() 