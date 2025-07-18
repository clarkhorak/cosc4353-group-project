from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.user import UserCreate, UserLogin, User
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Authentication service for user management and JWT handling"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # In-memory storage (replace with database later)
        self.users: Dict[str, Dict[str, Any]] = {}
        self.user_counter = 0
        
        # JWT configuration
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email = payload.get("sub")
            if email is None:
                return None
            return str(email)
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            return None
    
    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        if user_data.email in self.users:
            raise ValueError("User with this email already exists")
        
        # Create user
        self.user_counter += 1
        user_id = str(self.user_counter)
        hashed_password = self.hash_password(user_data.password)
        
        user = User(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=datetime.utcnow()
        )
        
        # Store user data
        self.users[user_data.email] = {
            "user": user,
            "hashed_password": hashed_password
        }
        
        logger.info(f"User registered successfully: {user_data.email}")
        return user
    
    def authenticate_user(self, login_data: UserLogin) -> Optional[str]:
        """Authenticate user and return JWT token"""
        user_data = self.users.get(login_data.email)
        if not user_data:
            logger.warning(f"Login attempt with non-existent email: {login_data.email}")
            return None
        
        if not self.verify_password(login_data.password, user_data["hashed_password"]):
            logger.warning(f"Invalid password for user: {login_data.email}")
            return None
        
        # Create access token
        token = self.create_access_token({"sub": login_data.email})
        logger.info(f"User authenticated successfully: {login_data.email}")
        return token
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_data = self.users.get(email)
        if user_data:
            return user_data["user"]
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        for user_data in self.users.values():
            if user_data["user"].id == user_id:
                return user_data["user"]
        return None
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user information"""
        for email, user_data in self.users.items():
            if user_data["user"].id == user_id:
                user = user_data["user"]
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                return user
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        for email, user_data in list(self.users.items()):
            if user_data["user"].id == user_id:
                del self.users[email]
                logger.info(f"User deleted: {email}")
                return True
        return False
    
    def get_all_users(self) -> list[User]:
        """Get all users (for admin purposes)"""
        return [user_data["user"] for user_data in self.users.values()]
    
    def is_user_active(self, email: str) -> bool:
        """Check if user is active"""
        user_data = self.users.get(email)
        if user_data:
            return user_data["user"].is_active
        return False
    
    def deactivate_user(self, email: str) -> bool:
        """Deactivate a user"""
        user_data = self.users.get(email)
        if user_data:
            user_data["user"].is_active = False
            logger.info(f"User deactivated: {email}")
            return True
        return False
    
    def activate_user(self, email: str) -> bool:
        """Activate a user"""
        user_data = self.users.get(email)
        if user_data:
            user_data["user"].is_active = True
            logger.info(f"User activated: {email}")
            return True
        return False 