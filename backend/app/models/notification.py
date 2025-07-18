from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    """Notification types"""
    EVENT_ASSIGNMENT = "event_assignment"
    EVENT_REMINDER = "event_reminder"
    NEW_EVENT = "new_event"
    STATUS_UPDATE = "status_update"
    SYSTEM_ANNOUNCEMENT = "system_announcement"

class NotificationBase(BaseModel):
    """Base notification model"""
    user_id: str
    type: NotificationType
    title: str
    message: str
    event_id: Optional[str] = None
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        if len(v) > 100:
            raise ValueError('Title cannot exceed 100 characters')
        return v.strip()
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Message must be at least 5 characters')
        if len(v) > 500:
            raise ValueError('Message cannot exceed 500 characters')
        return v.strip()

class NotificationCreate(NotificationBase):
    """Notification creation model"""
    pass

class Notification(BaseModel):
    """Complete notification model with metadata"""
    id: int
    user_id: str
    type: NotificationType
    title: str
    message: str
    event_id: Optional[str] = None
    created_at: datetime
    is_read: bool = False
    
    model_config = {
        "from_attributes": True
    }

class NotificationUpdate(BaseModel):
    """Notification update model"""
    is_read: bool

class NotificationResponse(BaseModel):
    """Notification response model"""
    id: int
    user_id: str
    type: NotificationType
    title: str
    message: str
    event_id: Optional[str] = None
    created_at: datetime
    is_read: bool
    
    model_config = {
        "from_attributes": True
    } 