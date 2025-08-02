from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.matching import EventSignup
from app.models.user import User
from app.services.matching_service import MatchingService
from app.utils.exceptions import ValidationError
from app.api.auth import get_current_user
from app.utils.rbac import admin_required

router = APIRouter(prefix="/matching", tags=["matching"])

# Shared instance for in-memory storage
_matching_service_instance = MatchingService()

def get_matching_service():
    return _matching_service_instance

@router.post("/signup", response_model=EventSignup, status_code=201)
@admin_required
async def signup_for_event(
    volunteer_id: str,
    event_id: int,
    current_user: User = Depends(get_current_user),
    matching_service: MatchingService = Depends(get_matching_service)
):
    """Sign up a volunteer for an event (admin only)"""
    try:
        return await matching_service.signup_for_event(volunteer_id, event_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/signup", status_code=204)
@admin_required
async def cancel_signup(
    volunteer_id: str,
    event_id: int,
    current_user: User = Depends(get_current_user),
    matching_service: MatchingService = Depends(get_matching_service)
):
    """Cancel a volunteer's signup for an event (admin only)"""
    try:
        await matching_service.cancel_signup(volunteer_id, event_id)
        return None
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/event/{event_id}", response_model=List[EventSignup])
@admin_required
async def list_signups_for_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    matching_service: MatchingService = Depends(get_matching_service)
):
    """List all signups for a specific event (admin only)"""
    return await matching_service.list_signups_for_event(event_id)

@router.get("/volunteer/{volunteer_id}", response_model=List[EventSignup])
async def list_signups_for_volunteer(
    volunteer_id: str,
    current_user: User = Depends(get_current_user),
    matching_service: MatchingService = Depends(get_matching_service)
):
    """List all signups for a specific volunteer (volunteers can see their own, admins can see all)"""
    # Volunteers can only see their own signups, admins can see any volunteer's signups
    if current_user.role == "volunteer" and current_user.id != volunteer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own signups"
        )
    return await matching_service.list_signups_for_volunteer(volunteer_id)

@router.post("/auto-match/{event_id}")
@admin_required
async def auto_match_volunteers(
    event_id: int,
    current_user: User = Depends(get_current_user),
    matching_service: MatchingService = Depends(get_matching_service)
):
    """Automatically match volunteers to an event based on skills and availability (admin only)"""
    try:
        matches = await matching_service.auto_match_volunteers(event_id)
        return {"message": f"Auto-matched {len(matches)} volunteers to event", "matches": matches}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) 