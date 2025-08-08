from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.profile import ProfileCreate, ProfileUpdate, Profile
from app.models.user import User
from app.services.profile_service import ProfileService
from app.api.auth import get_current_user
from app.utils.exceptions import ProfileNotFoundError, ValidationError

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("/", response_model=Profile, status_code=201)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends()
):
    """Create a new user profile"""
    try:
        user_id = int(current_user.id)
        # Prevent duplicate profiles for the same user
        try:
            existing_profile = await profile_service.get_profile(user_id)
            if existing_profile:
                raise HTTPException(status_code=400, detail="Profile already exists for this user")
        except ProfileNotFoundError:
            pass  # No profile exists, safe to create
        profile = await profile_service.create_profile(user_id, profile_data)
        return profile
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=Profile)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends()
):
    """Get current user's profile"""
    try:
        user_id = int(current_user.id)
        profile = await profile_service.get_profile(user_id)
        return profile
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{profile_id}", response_model=Profile)
async def get_profile(
    profile_id: int,
    profile_service: ProfileService = Depends()
):
    """Get profile by ID"""
    try:
        profile = await profile_service.get_profile_by_id(profile_id)
        return profile
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/me", response_model=Profile)
async def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends()
):
    """Update current user's profile"""
    try:
        user_id = int(current_user.id)
        profile = await profile_service.update_profile(user_id, profile_data)
        return profile
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/me", status_code=204)
async def delete_my_profile(
    current_user: User = Depends(get_current_user),
    profile_service: ProfileService = Depends()
):
    """Delete current user's profile"""
    try:
        user_id = int(current_user.id)
        await profile_service.delete_profile(user_id)
        return None
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[Profile])
async def get_all_profiles(
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of profiles to return"),
    profile_service: ProfileService = Depends()
):
    """Get all profiles with pagination"""
    profiles = await profile_service.get_all_profiles(skip=skip, limit=limit)
    return profiles


@router.get("/search/skills", response_model=List[Profile])
async def search_profiles_by_skills(
    skills: List[str] = Query(..., description="List of skills to search for"),
    profile_service: ProfileService = Depends()
):
    """Search profiles by skills"""
    profiles = await profile_service.search_profiles_by_skills(skills)
    return profiles


@router.get("/search/location", response_model=List[Profile])
async def search_profiles_by_location(
    city: str = Query(..., description="City to search in"),
    state: Optional[str] = Query(None, description="State to search in (optional)"),
    profile_service: ProfileService = Depends()
):
    """Search profiles by location"""
    profiles = await profile_service.search_profiles_by_location(city, state)
    return profiles