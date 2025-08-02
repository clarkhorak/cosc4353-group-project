from pydantic import BaseModel, field_validator
from typing import Optional, List
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
    required_skills: Optional[List[str]] = None
    urgency: str = "Medium"  # Low, Medium, High
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
        if len(v) > 200:
            raise ValueError('Location cannot exceed 200 characters')
        return v.strip()

    @field_validator('capacity')
    @classmethod
    def validate_capacity(cls, v):
        if v < 1:
            raise ValueError('Capacity must be at least 1')
        if v > 10000:
            raise ValueError('Capacity cannot exceed 10,000')
        return v

    @field_validator('urgency')
    @classmethod
    def validate_urgency(cls, v):
        allowed = {"Low", "Medium", "High"}
        if v not in allowed:
            raise ValueError(f'Urgency must be one of {allowed}')
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

    @field_validator('required_skills')
    @classmethod
    def validate_required_skills(cls, v):
        if v is not None:
            if len(v) > 10:
                raise ValueError('Cannot require more than 10 skills')
            
            # Validate against predefined skill list
            valid_skills = {
                'First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing',
                'Technical Support', 'Childcare', 'Elderly Care', 'Translation',
                'Event Planning', 'Fundraising', 'Marketing', 'Photography',
                'Videography', 'Music', 'Art', 'Sports', 'Tutoring'
            }
            
            invalid_skills = [skill for skill in v if skill not in valid_skills]
            if invalid_skills:
                raise ValueError(f'Invalid skills: {", ".join(invalid_skills)}')
        
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
    required_skills: Optional[List[str]] = None
    urgency: Optional[str] = None
    status: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,  # Enable ORM mode for SQLAlchemy objects
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Community Cleanup",
                "description": "Help clean up the local park",
                "category": "Environmental",
                "event_date": "2024-12-25",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "location": "Central Park",
                "capacity": 50,
                "requirements": "Bring gloves and bags",
                "status": "open",
                "urgency": "Medium",
                "required_skills": ["Organizing", "Teaching"],
                "created_at": "2024-12-01T10:00:00",
                "updated_at": "2024-12-01T10:00:00"
            }
        }
    } 