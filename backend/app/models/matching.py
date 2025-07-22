from pydantic import BaseModel, field_validator
from typing import Literal
from datetime import datetime

class EventSignup(BaseModel):
    event_id: int
    volunteer_id: str
    signup_time: datetime
    status: Literal["pending", "confirmed", "cancelled"] = "pending"

    @field_validator('volunteer_id')
    @classmethod
    def validate_volunteer_id(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('volunteer_id is required')
        return v.strip()

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed = {"pending", "confirmed", "cancelled"}
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v 