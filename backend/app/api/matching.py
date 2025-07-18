from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.matching import EventSignup
from app.services.matching_service import MatchingService
from app.utils.exceptions import ValidationError

router = APIRouter(prefix="/matching", tags=["matching"])

# Shared instance for in-memory storage
_matching_service_instance = MatchingService()

def get_matching_service():
    return _matching_service_instance

@router.post("/signup", response_model=EventSignup, status_code=201)
async def signup_for_event(
    volunteer_id: str,
    event_id: int,
    matching_service: MatchingService = Depends(get_matching_service)
):
    try:
        return await matching_service.signup_for_event(volunteer_id, event_id)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/signup", status_code=204)
async def cancel_signup(
    volunteer_id: str,
    event_id: int,
    matching_service: MatchingService = Depends(get_matching_service)
):
    try:
        await matching_service.cancel_signup(volunteer_id, event_id)
        return None
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/event/{event_id}", response_model=List[EventSignup])
async def list_signups_for_event(
    event_id: int,
    matching_service: MatchingService = Depends(get_matching_service)
):
    return await matching_service.list_signups_for_event(event_id)

@router.get("/volunteer/{volunteer_id}", response_model=List[EventSignup])
async def list_signups_for_volunteer(
    volunteer_id: str,
    matching_service: MatchingService = Depends(get_matching_service)
):
    return await matching_service.list_signups_for_volunteer(volunteer_id) 