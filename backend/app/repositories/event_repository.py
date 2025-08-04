import json
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_
from app.repositories.base_repository import BaseRepository
from app.models.database import Event

class EventRepository(BaseRepository[Event]):
    """Repository for Event model"""
    
    def __init__(self):
        super().__init__(Event)
    
    def get_by_title(self, title: str) -> Optional[Event]:
        """Get event by title"""
        session = self.get_session()
        try:
            stmt = select(Event).where(Event.title == title)
            result = session.execute(stmt)
            event = result.scalar_one_or_none()
            if event:
                session.refresh(event)
            return event
        finally:
            session.close()
    
    def search_events(self, search: str = None, category: str = None, 
                     status: str = None, urgency: str = None) -> List[Event]:
        """Search events with multiple filters"""
        session = self.get_session()
        try:
            conditions = []
            
            if search:
                conditions.append(
                    or_(
                        Event.title.ilike(f"%{search}%"),
                        Event.description.ilike(f"%{search}%"),
                        Event.location.ilike(f"%{search}%")
                    )
                )
            
            if category:
                conditions.append(Event.category.ilike(f"%{category}%"))
            
            if status:
                conditions.append(Event.status == status)
            
            if urgency:
                conditions.append(Event.urgency == urgency)
            
            if conditions:
                stmt = select(Event).where(and_(*conditions))
            else:
                stmt = select(Event)
            
            result = session.execute(stmt)
            events = result.scalars().all()
            # Refresh all events to ensure they're loaded
            for event in events:
                session.refresh(event)
            return events
        finally:
            session.close()
    
    def get_events_by_creator(self, created_by_id: str) -> List[Event]:
        """Get events created by a specific user"""
        session = self.get_session()
        try:
            stmt = select(Event).where(Event.created_by_id == created_by_id)
            result = session.execute(stmt)
            events = result.scalars().all()
            # Refresh all events to ensure they're loaded
            for event in events:
                session.refresh(event)
            return events
        finally:
            session.close()
    
    def get_open_events(self) -> List[Event]:
        """Get all open events"""
        session = self.get_session()
        try:
            stmt = select(Event).where(Event.status == "open")
            result = session.execute(stmt)
            events = result.scalars().all()
            # Refresh all events to ensure they're loaded
            for event in events:
                session.refresh(event)
            return events
        finally:
            session.close()
    
    def create_event(self, title: str, description: str, category: str,
                    event_date: str, start_time: str, end_time: str,
                    location: str, capacity: int, created_by_id: str,
                    requirements: Optional[str] = None, required_skills: Optional[List[str]] = None,
                    urgency: str = "Medium") -> Event:
        """Create a new event with proper data formatting"""
        # Convert required_skills to JSON string
        required_skills_json = json.dumps(required_skills) if required_skills else None
        
        event_data = {
            "title": title,
            "description": description,
            "category": category,
            "event_date": event_date,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "capacity": capacity,
            "created_by_id": created_by_id,
            "requirements": requirements,
            "required_skills": required_skills_json,
            "urgency": urgency,
            "status": "open"
        }
        
        return self.create(**event_data)
    
    def update_event(self, event_id: str, **kwargs) -> Optional[Event]:
        """Update event by ID"""
        # Handle required_skills conversion
        if "required_skills" in kwargs and isinstance(kwargs["required_skills"], list):
            kwargs["required_skills"] = json.dumps(kwargs["required_skills"])
        
        return self.update(event_id, **kwargs) 