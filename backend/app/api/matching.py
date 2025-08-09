from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models.matching import EventSignup
from app.models.user import User
from app.services.matching_service import MatchingService
from app.utils.exceptions import ValidationError
from app.api.auth import get_current_user
from app.utils.rbac import admin_required
from app.repositories.event_repository import EventRepository
from app.repositories.history_repository import HistoryRepository
from app.api.notification import get_notification_service
from app.models.notification import NotificationCreate, NotificationType

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


@router.post("/assign")
@admin_required
async def assign_volunteer_to_event(
    event_id: int,
    volunteer_id: Optional[str] = None,
    volunteer_email: Optional[str] = None,
    volunteer_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    """Assign a volunteer to an event (persisted in history). Admin only."""
    event_repo = EventRepository()
    history_repo = HistoryRepository()

    # Resolve hashed event_id to DB event
    db_event = None
    for e in event_repo.get_all():
        try:
            if hash(e.id) % 1000000 == event_id:
                db_event = e
                break
        except Exception:
            continue
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Determine volunteer user_id by id/email/name (prefer id, then email, then name)
    user_id = volunteer_id
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository()
    if not user_id and volunteer_email:
        user = user_repo.get_by_email(volunteer_email)
        if not user:
            raise HTTPException(status_code=404, detail="Volunteer with email not found")
        user_id = user.id
    if not user_id and volunteer_name:
        # naive lookup by name among active users
        for u in user_repo.get_active_users():
            if u.full_name.lower() == volunteer_name.lower():
                user_id = u.id
                break
        if not user_id:
            raise HTTPException(status_code=404, detail="Volunteer with name not found")

    # Prevent duplicate assignment
    existing = history_repo.get_by_user_and_event(user_id, db_event.id)
    if existing:
        return {"message": "Volunteer already assigned to this event"}

    # Create participation as confirmed
    participation = history_repo.create_participation(
        user_id=user_id,
        event_id=db_event.id,
        participation_date=db_event.event_date,
        hours_volunteered=0,
        status="completed",
    )

    # Send notification to volunteer about assignment
    notification_service = get_notification_service()
    await notification_service.create_notification(
        NotificationCreate(
            user_id=user_id,
            type=NotificationType.EVENT_ASSIGNMENT,
            title="Event assignment",
            message=f"You have been assigned to event '{db_event.title}' on {db_event.event_date}.",
            event_id=db_event.id,
        )
    )

    return {
        "message": "Volunteer assigned",
        "volunteer_id": user_id,
        "event_id": event_id,
        "participation_id": participation.id,
    }