import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.database import History

class HistoryRepository(BaseRepository[History]):
    """Repository for History model"""
    
    def __init__(self):
        super().__init__(History)
    
    def get_by_user_id(self, user_id: str) -> List[History]:
        """Get history by user ID"""
        session = self.get_session()
        try:
            stmt = select(History).where(History.user_id == user_id)
            result = session.execute(stmt)
            return result.scalars().all()
        finally:
            session.close()
    
    def get_by_user_and_event(self, user_id: str, event_id: str) -> Optional[History]:
        """Get history by user and event"""
        session = self.get_session()
        try:
            stmt = select(History).where(
                History.user_id == user_id,
                History.event_id == event_id
            )
            result = session.execute(stmt)
            return result.scalar_one_or_none()
        finally:
            session.close()
    
    def get_by_event_id(self, event_id: str) -> List[History]:
        """Get all history for an event"""
        session = self.get_session()
        try:
            stmt = select(History).where(History.event_id == event_id)
            result = session.execute(stmt)
            return result.scalars().all()
        finally:
            session.close()
    
    def get_active_participations(self, user_id: str) -> List[History]:
        """Get active participations for a user"""
        session = self.get_session()
        try:
            stmt = select(History).where(
                History.user_id == user_id,
                History.status == "completed"
            )
            result = session.execute(stmt)
            return result.scalars().all()
        finally:
            session.close()
    
    def create_participation(self, user_id: str, event_id: str, participation_date: str, hours_volunteered: int = 0, status: str = "completed") -> History:
        """Create a new participation record"""
        session = self.get_session()
        try:
            participation = History(
                user_id=user_id,
                event_id=event_id,
                participation_date=participation_date,
                hours_volunteered=hours_volunteered,
                status=status
            )
            session.add(participation)
            session.commit()
            session.refresh(participation)
            return participation
        finally:
            session.close()
    
    def update_participation(self, participation_id: str, **kwargs) -> Optional[History]:
        """Update a participation record"""
        return self.update(participation_id, **kwargs)
    
    def delete_participation(self, participation_id: str) -> bool:
        """Delete a participation record"""
        return self.delete(participation_id)
    
    def get_user_stats(self, user_id: str) -> dict:
        """Get volunteer statistics for a user"""
        session = self.get_session()
        try:
            # Get total hours
            total_hours_stmt = select(History.hours_volunteered).where(
                History.user_id == user_id,
                History.status == "completed"
            )
            total_hours_result = session.execute(total_hours_stmt)
            total_hours = sum(row[0] for row in total_hours_result.fetchall())
            
            # Get total events
            total_events_stmt = select(History).where(
                History.user_id == user_id,
                History.status == "completed"
            )
            total_events_result = session.execute(total_events_stmt)
            total_events = len(total_events_result.scalars().all())
            
            # Calculate average hours per event
            avg_hours = total_hours / total_events if total_events > 0 else 0
            
            return {
                "total_hours": total_hours,
                "total_events": total_events,
                "average_hours_per_event": avg_hours
            }
        finally:
            session.close() 