from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.models.user import User
from app.services.event_service import EventService
from app.api.auth import get_current_user
from app.utils.exceptions import ValidationError
from app.utils.rbac import admin_required
from app.api.notification import get_notification_service
from app.models.notification import NotificationCreate, NotificationType

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse, status_code=201)
@admin_required
async def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    event_service: EventService = Depends()
):
    """Create a new event (admin only)"""
    try:
        created = event_service.create_event(event_data, user_id=current_user.id)
        # Notify admins (or system) about new event - simple broadcast not implemented; skip for MVP
        return created
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0, description="Number of events to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of events to return"),
    search: Optional[str] = Query(None, description="Search term for event title or description"),
    category: Optional[str] = Query(None, description="Filter by event category"),
    status: Optional[str] = Query(None, description="Filter by event status"),
    event_service: EventService = Depends()
):
    """Get all events with optional filtering and pagination (all users can view)"""
    return event_service.list_events(
        skip=skip, 
        limit=limit, 
        search=search, 
        category=category, 
        status=status
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    event_service: EventService = Depends()
):
    """Get a specific event by ID (all users can view)"""
    try:
        return event_service.get_event(event_id)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{event_id}", response_model=EventResponse)
@admin_required
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    event_service: EventService = Depends()
):
    """Update an event (admin only)"""
    try:
        updated = event_service.update_event(event_id, event_data)
        # For MVP: no fanout; in a real system, notify enrolled volunteers
        return updated
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{event_id}", status_code=204)
@admin_required
async def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    event_service: EventService = Depends()
):
    """Delete an event (admin only)"""
    try:
        event_service.delete_event(event_id)
        return None
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e)) 