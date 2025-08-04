from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.user import UserCreate, UserLogin, User
from app.repositories.user_repository import UserRepository
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Authentication service for user management and JWT handling"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_repository = UserRepository()
        
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
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        hashed_password = self.hash_password(user_data.password)
        
        # Create user in database with role
        db_user = self.user_repository.create(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role=user_data.role,  # Added role field
            is_active=True
        )
        
        # Convert to User model for response
        user = User(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name,
            role=db_user.role,  # Added role field
            created_at=db_user.created_at,
            is_active=db_user.is_active
        )
        
        logger.info(f"User registered successfully: {user_data.email} with role: {user_data.role}")
        return user
    
    def authenticate_user(self, login_data: UserLogin) -> Optional[str]:
        """Authenticate user and return JWT token"""
        # Get user from database
        db_user = self.user_repository.get_by_email(login_data.email)
        if not db_user:
            logger.warning(f"Login attempt with non-existent email: {login_data.email}")
            return None
        
        if not self.verify_password(login_data.password, db_user.hashed_password):
            logger.warning(f"Invalid password for user: {login_data.email}")
            return None
        
        if not db_user.is_active:
            logger.warning(f"Login attempt for inactive user: {login_data.email}")
            return None
        
        # Create access token
        token = self.create_access_token({"sub": login_data.email})
        logger.info(f"User authenticated successfully: {login_data.email}")
        return token
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        db_user = self.user_repository.get_by_email(email)
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                full_name=db_user.full_name,
                role=db_user.role,  # Added role field
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        db_user = self.user_repository.get_by_id(user_id)
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                full_name=db_user.full_name,
                role=db_user.role,  # Added role field
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
        return None
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user"""
        db_user = self.user_repository.update(user_id, **kwargs)
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                full_name=db_user.full_name,
                role=db_user.role,  # Added role field
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        return self.user_repository.delete(user_id)
    
    def get_all_users(self) -> list[User]:
        """Get all users"""
        db_users = self.user_repository.get_all()
        return [
            User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                role=user.role,  # Added role field
                created_at=user.created_at,
                is_active=user.is_active
            )
            for user in db_users
        ]
    
    def is_user_active(self, email: str) -> bool:
        """Check if user is active"""
        user = self.get_user_by_email(email)
        return user.is_active if user else False
    
    def deactivate_user(self, email: str) -> bool:
        """Deactivate user"""
        user = self.get_user_by_email(email)
        if user:
            updated_user = self.update_user(user.id, is_active=False)
            return updated_user is not None
        return False
    
    def activate_user(self, email: str) -> bool:
        """Activate user"""
        user = self.get_user_by_email(email)
        if user:
            updated_user = self.update_user(user.id, is_active=True)
            return updated_user is not None
        return False
    
    def promote_to_admin(self, email: str) -> bool:
        """Promote user to admin role"""
        user = self.get_user_by_email(email)
        if user:
            updated_user = self.update_user(user.id, role="admin")
            logger.info(f"User promoted to admin: {email}")
            return updated_user is not None
        return False
    
    def demote_to_volunteer(self, email: str) -> bool:
        """Demote user to volunteer role"""
        user = self.get_user_by_email(email)
        if user:
            updated_user = self.update_user(user.id, role="volunteer")
            logger.info(f"User demoted to volunteer: {email}")
            return updated_user is not None
        return False
    
    def delete_user_by_email(self, email: str) -> bool:
        """Delete user by email"""
        user = self.get_user_by_email(email)
        if user:
            success = self.delete_user(user.id)
            if success:
                logger.info(f"User deleted: {email}")
            return success
        return False 