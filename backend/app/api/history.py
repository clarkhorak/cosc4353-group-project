from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from app.models.history import VolunteerHistory, VolunteerStats, ParticipationStatus
from app.services.history_service import HistoryService
from app.api.auth import get_current_user
from app.models.user import User
from app.utils.exceptions import ValidationError
from app.utils.rbac import admin_required
from app.services.event_service import EventService
from app.repositories.event_repository import EventRepository
from app.api.notification import get_notification_service
from app.models.notification import NotificationCreate, NotificationType

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/me", response_model=List[VolunteerHistory])
async def get_my_history(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(),
    event_repo: EventRepository = Depends()
):
    """Get current user's volunteer history with event details"""
    db_histories = history_service.history_repo.get_by_user_id(current_user.id)
    results: List[VolunteerHistory] = []
    for db_hist in db_histories:
        # Load event by original DB id
        db_event = event_repo.get_by_id(db_hist.event_id)
        if not db_event:
            # Skip if event not found
            continue
        # Build API model
        try:
            event_hashed_id = hash(str(db_event.id)) % 1000000
            hist_hashed_id = hash(str(db_hist.id)) % 1000000
        except Exception:
            event_hashed_id = 0
            hist_hashed_id = 0
        results.append(VolunteerHistory(
            id=hist_hashed_id,
            volunteer_id=db_hist.user_id,
            event_id=event_hashed_id,
            event_name=db_event.title,
            event_date=db_event.event_date,
            event_time=db_event.start_time,
            location=db_event.location,
            status=db_hist.status,  # FastAPI/Pydantic will coerce to enum
            joined_at=db_hist.created_at,
        ))
    return results


@router.get("/user/{user_id}", response_model=List[VolunteerHistory])
async def get_user_history(
    user_id: str,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Get volunteer history for a specific user (admin can view any user, volunteers can only view their own)"""
    # Volunteers can only see their own history, admins can see any user's history
    if current_user.role == "volunteer" and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own history"
        )
    return history_service.get_user_history(user_id)


@router.get("/stats", response_model=VolunteerStats)
async def get_stats(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Get current user's volunteer statistics"""
    # Call get_stats method which returns the correct format
    stats_data = history_service.get_stats(current_user.id)
    return VolunteerStats(**stats_data)


@router.get("/stats/{user_id}", response_model=VolunteerStats)
async def get_user_stats(
    user_id: str,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Get volunteer statistics for a specific user (admin can view any user, volunteers can only view their own)"""
    # Volunteers can only see their own stats, admins can see any user's stats
    if current_user.role == "volunteer" and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own statistics"
        )
    stats_data = history_service.get_stats(user_id)
    return VolunteerStats(**stats_data)


@router.post("/participate/{event_id}", response_model=VolunteerHistory)
async def participate(
    event_id: int,
    skills: Optional[List[str]] = Body(default=None),
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(),
    event_service: EventService = Depends(),
    event_repo: EventRepository = Depends()
):
    """Participate in an event"""
    try:
        # Resolve hashed event_id to original DB event
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

        # Persist participation
        db_hist = history_service.history_repo.create_participation(
            user_id=current_user.id,
            event_id=db_event.id,
            participation_date=db_event.event_date,
            hours_volunteered=0,
            status="completed",
        )

        # Notify volunteer of participation
        notification_service = get_notification_service()
        await notification_service.create_notification(
            NotificationCreate(
                user_id=current_user.id,
                type=NotificationType.EVENT_ASSIGNMENT,
                title="Event joined",
                message=f"You joined event '{db_event.title}' on {db_event.event_date}.",
                event_id=db_event.id,
            )
        )

        # Return API model with event details
        return VolunteerHistory(
            id=hash(str(db_hist.id)) % 1000000,
            volunteer_id=current_user.id,
            event_id=hash(str(db_event.id)) % 1000000,
            event_name=db_event.title,
            event_date=db_event.event_date,
            event_time=db_event.start_time,
            location=db_event.location,
            status=ParticipationStatus.COMPLETED,
            joined_at=db_hist.created_at,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{event_id}/status", response_model=VolunteerHistory)
async def update_status(
    event_id: int,
    status: ParticipationStatus,
    rating: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(),
    event_service: EventService = Depends(),
    event_repo: EventRepository = Depends()
):
    """Update participation status for an event"""
    try:
        # Resolve hashed event_id to original DB event
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

        # Find existing participation
        db_hist = history_service.history_repo.get_by_user_and_event(current_user.id, db_event.id)
        if not db_hist:
            raise HTTPException(status_code=404, detail="Participation not found")

        # Persist status update
        updated = history_service.history_repo.update_participation(db_hist.id, status=status.value)
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update participation")

        # Notify volunteer of status update
        notification_service = get_notification_service()
        await notification_service.create_notification(
            NotificationCreate(
                user_id=current_user.id,
                type=NotificationType.STATUS_UPDATE,
                title="Participation status updated",
                message=f"Your status for event '{db_event.title}' is now '{status.value}'.",
                event_id=db_event.id,
            )
        )

        return VolunteerHistory(
            id=hash(str(updated.id)) % 1000000,
            volunteer_id=updated.user_id,
            event_id=hash(str(db_event.id)) % 1000000,
            event_name=db_event.title,
            event_date=db_event.event_date,
            event_time=db_event.start_time,
            location=db_event.location,
            status=status,
            joined_at=updated.created_at
        )
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Admin-only endpoints
@router.get("/admin/all", response_model=List[VolunteerHistory])
@admin_required
async def get_all_history(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Get all volunteer history (admin only)"""
    return history_service.get_all_history()


@router.get("/admin/stats/overview")
@admin_required
async def get_overview_stats(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Get overview statistics for all volunteers (admin only)"""
    return history_service.get_overview_stats() 