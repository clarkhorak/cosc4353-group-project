from typing import List, Optional
from datetime import datetime
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.utils.exceptions import ValidationError

class EventService:
    def __init__(self):
        self.events: dict[int, EventResponse] = {}
        self.next_id = 1

    async def create_event(self, event_data: EventCreate) -> EventResponse:
        now = datetime.utcnow()
        event = EventResponse(
            id=self.next_id,
            title=event_data.title,
            description=event_data.description,
            category=event_data.category,
            event_date=event_data.event_date,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            location=event_data.location,
            capacity=event_data.capacity,
            requirements=event_data.requirements,
            status=event_data.status,
            created_at=now,
            updated_at=now
        )
        self.events[self.next_id] = event
        self.next_id += 1
        return event

    async def get_event(self, event_id: int) -> EventResponse:
        if event_id not in self.events:
            raise ValidationError(f"Event with ID {event_id} not found")
        return self.events[event_id]

    async def update_event(self, event_id: int, event_data: EventUpdate) -> EventResponse:
        if event_id not in self.events:
            raise ValidationError(f"Event with ID {event_id} not found")
        current = self.events[event_id]
        update_data = event_data.model_dump(exclude_unset=True)
        updated = EventResponse(
            **{**current.model_dump(), **update_data, "updated_at": datetime.utcnow()}
        )
        self.events[event_id] = updated
        return updated

    async def delete_event(self, event_id: int) -> bool:
        if event_id not in self.events:
            raise ValidationError(f"Event with ID {event_id} not found")
        del self.events[event_id]
        return True

    async def list_events(self, skip: int = 0, limit: int = 100, search: Optional[str] = None, category: Optional[str] = None, status: Optional[str] = None) -> List[EventResponse]:
        events = list(self.events.values())
        if search:
            events = [e for e in events if search.lower() in e.title.lower() or (e.description and search.lower() in e.description.lower())]
        if category:
            events = [e for e in events if e.category.lower() == category.lower()]
        if status:
            events = [e for e in events if e.status.lower() == status.lower()]
        return events[skip:skip+limit] 