from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.database import User

class UserRepository(BaseRepository[User]):
    """Repository for User model"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        session = self.get_session()
        try:
            stmt = select(User).where(User.email == email)
            result = session.execute(stmt)
            return result.scalar_one_or_none()
        finally:
            session.close()
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.get_by_email(email) is not None
    
    def get_active_users(self) -> List[User]:
        """Get all active users"""
        session = self.get_session()
        try:
            stmt = select(User).where(User.is_active == True)
            result = session.execute(stmt)
            return result.scalars().all()
        finally:
            session.close() 