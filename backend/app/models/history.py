from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time, datetime
from enum import Enum

class ParticipationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class VolunteerHistoryBase(BaseModel):
    volunteer_id: str
    event_id: int
    event_name: str
    event_date: date
    event_time: time
    location: str
    status: ParticipationStatus = ParticipationStatus.PENDING

class VolunteerHistoryCreate(VolunteerHistoryBase):
    pass

class VolunteerHistory(VolunteerHistoryBase):
    id: int
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }

class VolunteerHistoryUpdate(BaseModel):
    status: ParticipationStatus

class VolunteerStats(BaseModel):
    volunteer_id: str
    total_events: int
    completed_events: int
    pending_events: int
    cancelled_events: int
    no_show_events: int
    completion_rate: float

class EventParticipation(BaseModel):
    event_id: int
    event_name: str
    event_date: date
    event_time: time
    total_volunteers: int
    confirmed_volunteers: int
    completed_volunteers: int
    cancelled_volunteers: int
    no_show_volunteers: int

class ParticipateRequest(BaseModel):
    skills: Optional[list[str]] = None 