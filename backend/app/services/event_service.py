import json
from typing import List, Optional
from datetime import datetime
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.repositories.event_repository import EventRepository
from app.utils.exceptions import ValidationError

class EventService:
    def __init__(self):
        self.event_repo = EventRepository()

    def create_event(self, event_data: EventCreate, user_id: str = None) -> EventResponse:
        """Create a new event"""
        # Convert dates and times to strings
        event_date_str = event_data.event_date.isoformat()
        start_time_str = event_data.start_time.isoformat()
        end_time_str = event_data.end_time.isoformat()
        
        # Use provided user_id or default to "system"
        created_by_id = user_id or "system"
        
        # Create event in database
        db_event = self.event_repo.create_event(
            title=event_data.title,
            description=event_data.description,
            category=event_data.category,
            event_date=event_date_str,
            start_time=start_time_str,
            end_time=end_time_str,
            location=event_data.location,
            capacity=event_data.capacity,
            created_by_id=created_by_id,
            requirements=event_data.requirements,
            required_skills=event_data.required_skills,
            urgency=event_data.urgency
        )
        
        # Store the original database ID for later lookups
        db_event._original_id = db_event.id
        
        return self._db_to_pydantic_event(db_event)

    def get_event(self, event_id: int) -> EventResponse:
        """Get event by ID"""
        # We need to find the event by searching through all events
        # since we don't have a direct mapping from hash to UUID
        db_events = self.event_repo.get_all()
        
        # Find event by matching the hash
        target_hash = event_id
        db_event = None
        
        for event in db_events:
            try:
                event_hash = hash(event.id) % 1000000
                if event_hash == target_hash:
                    db_event = event
                    break
            except (ValueError, TypeError):
                continue
        
        if not db_event:
            raise ValidationError(f"Event with ID {event_id} not found")
        
        # Extract all attributes immediately while the session is still open
        # This prevents detached session issues
        event_data = {
            'id': db_event.id,
            'title': db_event.title,
            'description': db_event.description,
            'category': db_event.category,
            'event_date': db_event.event_date,
            'start_time': db_event.start_time,
            'end_time': db_event.end_time,
            'location': db_event.location,
            'capacity': db_event.capacity,
            'requirements': db_event.requirements,
            'required_skills': db_event.required_skills,
            'urgency': db_event.urgency,
            'status': db_event.status,
            'created_at': db_event.created_at,
            'updated_at': db_event.updated_at
        }
        
        # Parse required_skills from JSON if necessary
        if isinstance(event_data['required_skills'], str):
            try:
                required_skills = json.loads(event_data['required_skills'])
            except (json.JSONDecodeError, TypeError):
                required_skills = []
        else:
            required_skills = event_data['required_skills'] or []

        # Convert ID to int if possible, otherwise use a hash
        try:
            event_id_int = int(event_data['id'])
        except (ValueError, TypeError):
            event_id_int = hash(str(event_data['id'])) % 1000000

        # Create EventResponse with extracted data
        return EventResponse(
            id=event_id_int,
            title=event_data['title'],
            description=event_data['description'],
            category=event_data['category'],
            event_date=event_data['event_date'],
            start_time=event_data['start_time'],
            end_time=event_data['end_time'],
            location=event_data['location'],
            capacity=event_data['capacity'],
            requirements=event_data['requirements'],
            required_skills=required_skills,
            urgency=event_data['urgency'],
            status=event_data['status'],
            created_at=event_data['created_at'],
            updated_at=event_data['updated_at']
        )

    def update_event(self, event_id: int, event_data: EventUpdate) -> EventResponse:
        """Update event by ID"""
        # Find event by searching through all events
        db_events = self.event_repo.get_all()
        
        # Find event by matching the hash
        target_hash = event_id
        db_event = None
        
        for event in db_events:
            try:
                event_hash = hash(event.id) % 1000000
                if event_hash == target_hash:
                    db_event = event
                    break
            except (ValueError, TypeError):
                continue
        
        if not db_event:
            raise ValidationError(f"Event with ID {event_id} not found")
        
        # Prepare update data
        update_data = {}
        
        if event_data.title:
            update_data["title"] = event_data.title
        
        if event_data.description:
            update_data["description"] = event_data.description
        
        if event_data.category:
            update_data["category"] = event_data.category
        
        if event_data.event_date:
            update_data["event_date"] = event_data.event_date.isoformat()
        
        if event_data.start_time:
            update_data["start_time"] = event_data.start_time.isoformat()
        
        if event_data.end_time:
            update_data["end_time"] = event_data.end_time.isoformat()
        
        if event_data.location:
            update_data["location"] = event_data.location
        
        if event_data.capacity:
            update_data["capacity"] = event_data.capacity
        
        if event_data.requirements:
            update_data["requirements"] = event_data.requirements
        
        if event_data.required_skills:
            update_data["required_skills"] = event_data.required_skills
        
        if event_data.urgency:
            update_data["urgency"] = event_data.urgency
        
        if event_data.status:
            update_data["status"] = event_data.status
        
        # Update in database using the original ID
        updated_event = self.event_repo.update_event(db_event.id, **update_data)
        
        if not updated_event:
            raise ValidationError(f"Event with ID {event_id} not found")
        
        return self._db_to_pydantic_event(updated_event)

    def delete_event(self, event_id: int) -> bool:
        """Delete event by ID"""
        # Find event by searching through all events
        db_events = self.event_repo.get_all()
        
        # Find event by matching the hash
        target_hash = event_id
        db_event = None
        
        for event in db_events:
            try:
                event_hash = hash(event.id) % 1000000
                if event_hash == target_hash:
                    db_event = event
                    break
            except (ValueError, TypeError):
                continue
        
        if not db_event:
            raise ValidationError(f"Event with ID {event_id} not found")
        
        return self.event_repo.delete(db_event.id)

    def list_events(self, skip: int = 0, limit: int = 100, search: Optional[str] = None, 
                   category: Optional[str] = None, status: Optional[str] = None) -> List[EventResponse]:
        """List events with filters"""
        db_events = self.event_repo.search_events(
            search=search,
            category=category,
            status=status
        )
        
        # Apply pagination
        paginated_events = db_events[skip:skip + limit]
        return [self._db_to_pydantic_event(event) for event in paginated_events]

    def _db_to_pydantic_event(self, db_event) -> EventResponse:
        """Convert database event to Pydantic event response"""
        
        # Parse required_skills from JSON if necessary
        if isinstance(db_event.required_skills, str):
            try:
                required_skills = json.loads(db_event.required_skills)
            except (json.JSONDecodeError, TypeError):
                required_skills = []
        else:
            required_skills = db_event.required_skills or []

        # Convert ID to int if possible, otherwise use a hash
        try:
            event_id = int(db_event.id)
        except (ValueError, TypeError):
            event_id = hash(str(db_event.id)) % 1000000

        # Build safe dict with all needed fields - extract everything before session closes
        return EventResponse(
            id=event_id,
            title=db_event.title,
            description=db_event.description,
            category=db_event.category,
            event_date=db_event.event_date,
            start_time=db_event.start_time,
            end_time=db_event.end_time,
            location=db_event.location,
            capacity=db_event.capacity,
            requirements=db_event.requirements,
            required_skills=required_skills,
            urgency=db_event.urgency,
            status=db_event.status,
            created_at=db_event.created_at,
            updated_at=db_event.updated_at
        ) 