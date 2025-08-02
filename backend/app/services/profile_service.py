import json
from typing import Optional, List
from datetime import datetime
from app.models.profile import ProfileCreate, ProfileUpdate, Profile, Address, Availability
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.utils.exceptions import ProfileNotFoundError, ValidationError


class ProfileService:
    def __init__(self):
        self.profile_repo = ProfileRepository()
    
    def create_profile(self, user_id: int, profile_data: ProfileCreate) -> Profile:
        """Create a new user profile"""
        user_id_str = str(user_id)
        
        # Check if profile already exists
        if self.profile_repo.user_has_profile(user_id_str):
            raise ValidationError("Profile already exists for this user")
        
        # Convert availability to list of dicts
        availability_list = []
        for avail in profile_data.availability:
            availability_list.append({
                "date": avail.date.isoformat(),
                "time": avail.time.isoformat()
            })
        
        # Create profile in database
        db_profile = self.profile_repo.create_profile(
            user_id=user_id_str,
            address_data={
                "address1": profile_data.address.address1,
                "city": profile_data.address.city,
                "state_code": profile_data.address.state_code,
                "zip_code": profile_data.address.zip_code
            },
            skills=profile_data.skills,
            availability=availability_list,
            preferences=profile_data.preferences
        )
        
        # Convert back to Pydantic model for response
        return self._db_to_pydantic_profile(db_profile)
    
    def get_profile(self, user_id: int) -> Profile:
        """Get user profile by user ID"""
        user_id_str = str(user_id)
        db_profile = self.profile_repo.get_by_user_id(user_id_str)
        
        if not db_profile:
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        return self._db_to_pydantic_profile(db_profile)
    
    def get_profile_by_id(self, profile_id: int) -> Profile:
        """Get profile by profile ID"""
        db_profile = self.profile_repo.get_by_id(str(profile_id))
        
        if not db_profile:
            raise ProfileNotFoundError(f"Profile with ID {profile_id} not found")
        
        return self._db_to_pydantic_profile(db_profile)
    
    def update_profile(self, user_id: int, profile_data: ProfileUpdate) -> Profile:
        """Update user profile"""
        user_id_str = str(user_id)
        
        # Check if profile exists
        if not self.profile_repo.user_has_profile(user_id_str):
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        # Prepare update data
        update_data = {}
        
        if profile_data.address:
            update_data.update({
                "address1": profile_data.address.address1,
                "city": profile_data.address.city,
                "state_code": profile_data.address.state_code,
                "zip_code": profile_data.address.zip_code
            })
        
        if profile_data.skills:
            update_data["skills"] = profile_data.skills
        
        if profile_data.availability:
            availability_list = []
            for avail in profile_data.availability:
                availability_list.append({
                    "date": avail.date.isoformat(),
                    "time": avail.time.isoformat()
                })
            update_data["availability"] = availability_list
        
        if profile_data.preferences is not None:
            update_data["preferences"] = profile_data.preferences
        
        # Update in database
        db_profile = self.profile_repo.update_profile(user_id_str, **update_data)
        
        if not db_profile:
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        return self._db_to_pydantic_profile(db_profile)
    
    def delete_profile(self, user_id: int) -> bool:
        """Delete user profile"""
        user_id_str = str(user_id)
        db_profile = self.profile_repo.get_by_user_id(user_id_str)
        
        if not db_profile:
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        return self.profile_repo.delete(db_profile.id)
    
    def get_all_profiles(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Get all profiles with pagination"""
        db_profiles = self.profile_repo.get_all(skip=skip, limit=limit)
        return [self._db_to_pydantic_profile(p) for p in db_profiles]
    
    def search_profiles_by_skills(self, skills: List[str]) -> List[Profile]:
        """Search profiles by skills"""
        db_profiles = self.profile_repo.search_by_skills(skills)
        return [self._db_to_pydantic_profile(p) for p in db_profiles]
    
    def search_profiles_by_location(self, city: str, state: Optional[str] = None) -> List[Profile]:
        """Search profiles by location"""
        db_profiles = self.profile_repo.search_by_location(city, state)
        return [self._db_to_pydantic_profile(p) for p in db_profiles]
    
    def _db_to_pydantic_profile(self, db_profile) -> Profile:
        """Convert database profile to Pydantic profile"""
        # Parse skills and availability from JSON
        skills = json.loads(db_profile.skills) if db_profile.skills else []
        availability_data = json.loads(db_profile.availability) if db_profile.availability else []
        
        # Convert availability data back to Pydantic models
        availability = []
        for avail_data in availability_data:
            from datetime import date, time
            avail_date = date.fromisoformat(avail_data["date"])
            avail_time = time.fromisoformat(avail_data["time"])
            availability.append(Availability(date=avail_date, time=avail_time))
        
        # Create address object
        address = Address(
            address1=db_profile.address1,
            city=db_profile.city,
            state_code=db_profile.state_code,
            zip_code=db_profile.zip_code
        )
        
        return Profile(
            user_id=db_profile.user_id,
            address=address,
            skills=skills,
            preferences=db_profile.preferences,
            availability=availability
        ) 