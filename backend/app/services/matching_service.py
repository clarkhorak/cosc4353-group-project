from typing import List
from datetime import datetime
from app.models.matching import EventSignup
from app.utils.exceptions import ValidationError

class MatchingService:
    def __init__(self):
        self.signups: List[EventSignup] = []

    async def signup_for_event(self, volunteer_id: str, event_id: int) -> EventSignup:
        # Prevent duplicate signups
        for s in self.signups:
            if s.volunteer_id == volunteer_id and s.event_id == event_id and s.status == "pending":
                raise ValidationError("Already signed up for this event.")
        signup = EventSignup(
            event_id=event_id,
            volunteer_id=volunteer_id,
            signup_time=datetime.utcnow(),
            status="pending"
        )
        self.signups.append(signup)
        return signup

    async def cancel_signup(self, volunteer_id: str, event_id: int) -> bool:
        for s in self.signups:
            if s.volunteer_id == volunteer_id and s.event_id == event_id and s.status == "pending":
                s.status = "cancelled"
                return True
        raise ValidationError("Signup not found or already cancelled.")

    async def list_signups_for_event(self, event_id: int) -> List[EventSignup]:
        return [s for s in self.signups if s.event_id == event_id and s.status == "pending"]

    async def list_signups_for_volunteer(self, volunteer_id: str) -> List[EventSignup]:
        return [s for s in self.signups if s.volunteer_id == volunteer_id and s.status == "pending"] 