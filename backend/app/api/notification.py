from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.notification import NotificationCreate, NotificationResponse
from app.services.notification_service import NotificationService
from app.utils.exceptions import ValidationError

router = APIRouter(prefix="/notifications", tags=["notifications"])

# Shared instance for in-memory storage
_notification_service_instance = NotificationService()

def get_notification_service():
    return _notification_service_instance

@router.post("/", response_model=NotificationResponse, status_code=201)
async def create_notification(
    data: NotificationCreate,
    notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        return await notification_service.create_notification(data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications_for_user(
    user_id: str = Query(...),
    notification_service: NotificationService = Depends(get_notification_service)
):
    return await notification_service.list_notifications_for_user(user_id)

@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        return await notification_service.mark_as_read(notification_id)
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{notification_id}", status_code=204)
async def delete_notification(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service)
):
    try:
        await notification_service.delete_notification(notification_id)
        return None
    except ValidationError as e:
        raise HTTPException(status_code=404, detail=str(e)) 