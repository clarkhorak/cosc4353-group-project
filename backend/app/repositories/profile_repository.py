import json
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.repositories.base_repository import BaseRepository
from app.models.database import Profile

class ProfileRepository(BaseRepository[Profile]):
    """Repository for Profile model"""
    
    def __init__(self):
        super().__init__(Profile)
    
    def get_by_user_id(self, user_id: str) -> Optional[Profile]:
        """Get profile by user ID"""
        session = self.get_session()
        try:
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = session.execute(stmt)
            return result.scalar_one_or_none()
        finally:
            session.close()
    
    def user_has_profile(self, user_id: str) -> bool:
        """Check if user has a profile"""
        return self.get_by_user_id(user_id) is not None
    
    def search_by_skills(self, skills: List[str]) -> List[Profile]:
        """Search profiles by skills"""
        session = self.get_session()
        try:
            # Convert skills list to JSON string for searching
            skill_conditions = []
            for skill in skills:
                skill_conditions.append(Profile.skills.contains(skill))
            
            stmt = select(Profile).where(or_(*skill_conditions))
            result = session.execute(stmt)
            return result.scalars().all()
        finally:
            session.close()
    
    def search_by_location(self, city: str, state: Optional[str] = None) -> List[Profile]:
        """Search profiles by location"""
        session = self.get_session()
        try:
            conditions = [Profile.city.ilike(f"%{city}%")]
            if state:
                conditions.append(Profile.state_code.ilike(f"%{state}%"))
            
            stmt = select(Profile).where(or_(*conditions))
            result = session.execute(stmt)
            return result.scalars().all()
        finally:
            session.close()
    
    def create_profile(self, user_id: str, address_data: dict, skills: List[str], 
                      availability: List[dict], preferences: Optional[str] = None) -> Profile:
        """Create a new profile with proper data formatting"""
        # Convert skills and availability to JSON strings
        skills_json = json.dumps(skills)
        availability_json = json.dumps(availability)
        
        profile_data = {
            "user_id": user_id,
            "address1": address_data["address1"],
            "city": address_data["city"],
            "state_code": address_data["state_code"],
            "zip_code": address_data["zip_code"],
            "skills": skills_json,
            "availability": availability_json,
            "preferences": preferences
        }
        
        return self.create(**profile_data)
    
    def update_profile(self, user_id: str, **kwargs) -> Optional[Profile]:
        """Update profile by user ID"""
        profile = self.get_by_user_id(user_id)
        if not profile:
            return None
        
        # Handle skills and availability conversion
        if "skills" in kwargs and isinstance(kwargs["skills"], list):
            kwargs["skills"] = json.dumps(kwargs["skills"])
        
        if "availability" in kwargs and isinstance(kwargs["availability"], list):
            kwargs["availability"] = json.dumps(kwargs["availability"])
        
        return self.update(profile.id, **kwargs)
    
    def delete_by_user_id(self, user_id: str) -> bool:
        """Delete profile by user ID"""
        profile = self.get_by_user_id(user_id)
        if not profile:
            return False
        
        return self.delete(profile.id) 