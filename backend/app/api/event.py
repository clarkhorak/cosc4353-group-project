from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.services.event_service import EventService
from app.utils.exceptions import ValidationError

router = APIRouter(prefix="/events", tags=["events"])

# Shared instance for in-memory storage
_event_service_instance = EventService()

def get_event_service():
    return _event_service_instance

@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(
    event_data: EventCreate,
    event_service: EventService = Depends(get_event_service)
):
    try:
        return await event_service.create_event(event_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    event_service: EventService = Depends(get_event_service)
):
    return await event_service.list_events(skip=skip, limit=limit, search=search, category=category, status=status)

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    event_service: EventService = Depends(get_event_service)
):
    try:
        return await event_service.get_event(event_id)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    event_service: EventService = Depends(get_event_service)
):
    try:
        return await event_service.update_event(event_id, event_data)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: int,
    event_service: EventService = Depends(get_event_service)
):
    try:
        await event_service.delete_event(event_id)
        return None
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e)) 