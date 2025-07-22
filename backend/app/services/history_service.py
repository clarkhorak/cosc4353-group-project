from typing import List, Optional, Dict
from datetime import datetime, date, time
from app.models.history import (
    VolunteerHistoryBase, VolunteerHistoryCreate, VolunteerHistory, VolunteerHistoryUpdate, VolunteerStats, ParticipationStatus, EventParticipation
)
from app.utils.exceptions import ValidationError

class HistoryService:
    def __init__(self):
        self.histories: Dict[str, List[VolunteerHistory]] = {}  # user_id -> list of participations
        self.next_id = 1
        # Mock event data for testing
        self.mock_events = {
            1: {"name": "Community Cleanup", "date": date(2025, 12, 25), "time": time(14, 0), "location": "Central Park"},
            2: {"name": "Food Drive", "date": date(2025, 12, 26), "time": time(10, 0), "location": "Community Center"}
        }

    async def participate(self, user_id: str, event_id: int) -> VolunteerHistory:
        # Prevent duplicate participation
        user_histories = self.histories.setdefault(user_id, [])
        for h in user_histories:
            if h.event_id == event_id:
                raise ValidationError("Already participating in this event.")
        
        # Get event details
        event_data = self.mock_events.get(event_id, {
            "name": f"Event {event_id}",
            "date": date(2025, 12, 25),
            "time": time(14, 0),
            "location": "Unknown Location"
        })
        
        history = VolunteerHistory(
            id=self.next_id,
            volunteer_id=user_id,
            event_id=event_id,
            event_name=event_data["name"],
            event_date=event_data["date"],
            event_time=event_data["time"],
            location=event_data["location"],
            status=ParticipationStatus.PENDING,
            joined_at=datetime.utcnow()
        )
        user_histories.append(history)
        self.next_id += 1
        return history

    async def update_status(self, user_id: str, event_id: int, status: ParticipationStatus) -> VolunteerHistory:
        user_histories = self.histories.get(user_id, [])
        for h in user_histories:
            if h.event_id == event_id:
                h.status = status
                return h
        raise ValidationError("Participation not found.")

    async def get_history(self, user_id: str) -> List[VolunteerHistory]:
        return self.histories.get(user_id, [])

    async def get_stats(self, user_id: str) -> VolunteerStats:
        histories = self.histories.get(user_id, [])
        total_events = len(histories)
        completed_events = len([h for h in histories if h.status == ParticipationStatus.COMPLETED])
        pending_events = len([h for h in histories if h.status == ParticipationStatus.PENDING])
        cancelled_events = len([h for h in histories if h.status == ParticipationStatus.CANCELLED])
        no_show_events = len([h for h in histories if h.status == ParticipationStatus.NO_SHOW])
        completion_rate = completed_events / total_events if total_events else 0.0
        
        return VolunteerStats(
            volunteer_id=user_id,
            total_events=total_events,
            completed_events=completed_events,
            pending_events=pending_events,
            cancelled_events=cancelled_events,
            no_show_events=no_show_events,
            completion_rate=completion_rate
        ) 