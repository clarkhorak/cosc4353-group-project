from typing import Optional, List
from datetime import datetime
from app.models.profile import ProfileCreate, ProfileUpdate, Profile
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.exceptions import ProfileNotFoundError, ValidationError


class ProfileService:
    def __init__(self):
        self.auth_service = AuthService()
        # In-memory storage for profiles (replace with database in production)
        self.profiles: dict[int, Profile] = {}
    
    async def create_profile(self, user_id: int, profile_data: ProfileCreate) -> Profile:
        """Create a new user profile"""
        # Check if profile already exists
        if user_id in self.profiles:
            raise ValidationError("Profile already exists for this user")
        
        # Create profile
        profile = Profile(
            user_id=str(user_id),
            address=profile_data.address,
            skills=profile_data.skills,
            preferences=profile_data.preferences,
            availability=profile_data.availability
        )
        
        self.profiles[user_id] = profile
        return profile
    
    async def get_profile(self, user_id: int) -> Profile:
        """Get user profile by user ID"""
        if user_id not in self.profiles:
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        return self.profiles[user_id]
    
    async def get_profile_by_id(self, profile_id: int) -> Profile:
        """Get profile by profile ID"""
        if profile_id not in self.profiles:
            raise ProfileNotFoundError(f"Profile with ID {profile_id} not found")
        
        return self.profiles[profile_id]
    
    async def update_profile(self, user_id: int, profile_data: ProfileUpdate) -> Profile:
        """Update user profile"""
        if user_id not in self.profiles:
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        current_profile = self.profiles[user_id]
        
        # Update only provided fields
        update_data = profile_data.model_dump(exclude_unset=True)
        
        # Create updated profile
        updated_profile = Profile(
            **{**current_profile.model_dump(), **update_data}
        )
        
        self.profiles[user_id] = updated_profile
        return updated_profile
    
    async def delete_profile(self, user_id: int) -> bool:
        """Delete user profile"""
        if user_id not in self.profiles:
            raise ProfileNotFoundError(f"Profile not found for user {user_id}")
        
        del self.profiles[user_id]
        return True
    
    async def get_all_profiles(self, skip: int = 0, limit: int = 100) -> List[Profile]:
        """Get all profiles with pagination"""
        profiles = list(self.profiles.values())
        return profiles[skip:skip + limit]
    
    async def search_profiles_by_skills(self, skills: List[str]) -> List[Profile]:
        """Search profiles by skills"""
        matching_profiles = []
        for profile in self.profiles.values():
            if any(skill.lower() in [s.lower() for s in profile.skills] for skill in skills):
                matching_profiles.append(profile)
        return matching_profiles
    
    async def search_profiles_by_location(self, city: str, state: Optional[str] = None) -> List[Profile]:
        """Search profiles by location"""
        matching_profiles = []
        for profile in self.profiles.values():
            if (profile.address.city.lower() == city.lower() and 
                (state is None or profile.address.state.lower() == state.lower())):
                matching_profiles.append(profile)
        return matching_profiles 