from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.history import VolunteerHistory, VolunteerStats, ParticipationStatus, ParticipateRequest
from app.services.history_service import HistoryService
from app.api.auth import get_current_user
from app.models.user import User
from app.utils.exceptions import ValidationError

router = APIRouter(prefix="/history", tags=["history"])

_history_service_instance = HistoryService()

def get_history_service():
    return _history_service_instance

@router.get("/", response_model=List[VolunteerHistory])
async def get_history(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(get_history_service)
):
    return await history_service.get_history(current_user.id)

@router.get("/stats", response_model=VolunteerStats)
async def get_stats(
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(get_history_service)
):
    return await history_service.get_stats(current_user.id)

@router.post("/participate/{event_id}", response_model=VolunteerHistory)
async def participate(
    event_id: int,
    request: ParticipateRequest,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(get_history_service)
):
    try:
        return await history_service.participate(current_user.id, event_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{event_id}/status", response_model=VolunteerHistory)
async def update_status(
    event_id: int,
    status: ParticipationStatus,
    rating: Optional[float] = None,
    current_user: User = Depends(get_current_user),
    history_service: HistoryService = Depends(get_history_service)
):
    try:
        return await history_service.update_status(current_user.id, event_id, status, rating)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e)) 