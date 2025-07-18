from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time, datetime
import re

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    event_date: date
    start_time: time
    end_time: time
    location: str
    capacity: int
    requirements: Optional[str] = None
    status: str = "open"  # open, closed, cancelled

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        if len(v) > 100:
            raise ValueError('Title cannot exceed 100 characters')
        return v.strip()

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Category must be at least 3 characters')
        if len(v) > 50:
            raise ValueError('Category cannot exceed 50 characters')
        return v.strip()

    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Location must be at least 3 characters')
        if len(v) > 100:
            raise ValueError('Location cannot exceed 100 characters')
        return v.strip()

    @field_validator('capacity')
    @classmethod
    def validate_capacity(cls, v):
        if v < 1:
            raise ValueError('Capacity must be at least 1')
        if v > 10000:
            raise ValueError('Capacity cannot exceed 10,000')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed = {"open", "closed", "cancelled"}
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v

    @field_validator('end_time')
    @classmethod
    def validate_times(cls, v, info):
        start_time = info.data.get('start_time')
        if start_time and v <= start_time:
            raise ValueError('End time must be after start time')
        return v

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    event_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    requirements: Optional[str] = None
    status: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    } 