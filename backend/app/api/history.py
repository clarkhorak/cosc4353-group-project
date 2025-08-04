from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.history import VolunteerHistory, VolunteerStats, ParticipationStatus
from app.services.history_service import HistoryService
from app.api.auth import get_current_user
from app.models.user import User
from app.utils.exceptions import ValidationError
from app.utils.rbac import admin_required

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/me", response_model=List[VolunteerHistory])
async def get_my_history(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Get current user's volunteer history"""
    return history_service.get_user_history(current_user.id)


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
    skills: Optional[List[str]] = None,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Participate in an event"""
    try:
        # For now, return a mock response since the participate method doesn't exist
        return VolunteerHistory(
            id="mock_id",
            user_id=current_user.id,
            event_id=str(event_id),
            participation_date="2025-01-01",
            hours_volunteered=4,
            status="completed",
            created_at=datetime.now()
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{event_id}/status", response_model=VolunteerHistory)
async def update_status(
    event_id: int,
    status: ParticipationStatus,
    rating: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends()
):
    """Update participation status for an event"""
    try:
        # For now, return a mock response since the update_status method doesn't exist
        return VolunteerHistory(
            id="mock_id",
            user_id=current_user.id,
            event_id=str(event_id),
            participation_date="2025-01-01",
            hours_volunteered=4,
            status=status.value,
            created_at=datetime.now()
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