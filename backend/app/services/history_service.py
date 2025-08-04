from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.history import VolunteerHistoryCreate, VolunteerHistory, VolunteerHistoryUpdate, VolunteerStats
from app.repositories.history_repository import HistoryRepository
import logging

logger = logging.getLogger(__name__)

class HistoryService:
    """Service for managing volunteer history and participation"""
    
    def __init__(self):
        self.history_repo = HistoryRepository()
    
    def record_participation(self, user_id: str, event_id: str, participation_date: str, hours_volunteered: int = 0, status: str = "completed") -> VolunteerHistory:
        """Record a new volunteer participation"""
        try:
            # Create participation record
            db_history = self.history_repo.create_participation(
                user_id=user_id,
                event_id=event_id,
                participation_date=participation_date,
                hours_volunteered=hours_volunteered,
                status=status
            )
            
            # Convert to response model
            history = VolunteerHistory(
                id=db_history.id,
                user_id=db_history.user_id,
                event_id=db_history.event_id,
                participation_date=db_history.participation_date,
                hours_volunteered=db_history.hours_volunteered,
                status=db_history.status,
                created_at=db_history.created_at
            )
            
            logger.info(f"Participation recorded for user {user_id} in event {event_id}")
            return history
            
        except Exception as e:
            logger.error(f"Error recording participation: {e}")
            raise
    
    def get_user_history(self, user_id: str) -> List[VolunteerHistory]:
        """Get all participation history for a user"""
        try:
            db_histories = self.history_repo.get_by_user_id(user_id)
            
            histories = []
            for db_history in db_histories:
                history = VolunteerHistory(
                    id=db_history.id,
                    user_id=db_history.user_id,
                    event_id=db_history.event_id,
                    participation_date=db_history.participation_date,
                    hours_volunteered=db_history.hours_volunteered,
                    status=db_history.status,
                    created_at=db_history.created_at
                )
                histories.append(history)
            
            return histories
            
        except Exception as e:
            logger.error(f"Error getting user history: {e}")
            raise
    
    def get_event_participation(self, event_id: str) -> List[VolunteerHistory]:
        """Get all participation records for an event"""
        try:
            db_histories = self.history_repo.get_by_event_id(event_id)
            
            histories = []
            for db_history in db_histories:
                history = VolunteerHistory(
                    id=db_history.id,
                    user_id=db_history.user_id,
                    event_id=db_history.event_id,
                    participation_date=db_history.participation_date,
                    hours_volunteered=db_history.hours_volunteered,
                    status=db_history.status,
                    created_at=db_history.created_at
                )
                histories.append(history)
            
            return histories
            
        except Exception as e:
            logger.error(f"Error getting event participation: {e}")
            raise
    
    def update_participation(self, participation_id: str, update_data: VolunteerHistoryUpdate) -> Optional[VolunteerHistory]:
        """Update a participation record"""
        try:
            db_history = self.history_repo.update_participation(participation_id, **update_data.model_dump(exclude_unset=True))
            
            if db_history:
                history = VolunteerHistory(
                    id=db_history.id,
                    user_id=db_history.user_id,
                    event_id=db_history.event_id,
                    participation_date=db_history.participation_date,
                    hours_volunteered=db_history.hours_volunteered,
                    status=db_history.status,
                    created_at=db_history.created_at
                )
                return history
            
            return None
            
        except Exception as e:
            logger.error(f"Error updating participation: {e}")
            raise
    
    def delete_participation(self, participation_id: str) -> bool:
        """Delete a participation record"""
        try:
            return self.history_repo.delete_participation(participation_id)
        except Exception as e:
            logger.error(f"Error deleting participation: {e}")
            raise
    
    def get_user_stats(self, user_id: str) -> VolunteerStats:
        """Get volunteer statistics for a user"""
        try:
            stats_data = self.history_repo.get_user_stats(user_id)
            
            stats = VolunteerStats(
                total_hours=stats_data["total_hours"],
                total_events=stats_data["total_events"],
                average_hours_per_event=stats_data["average_hours_per_event"]
            )
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            raise
    
    def get_active_participations(self, user_id: str) -> List[VolunteerHistory]:
        """Get active participation records for a user"""
        try:
            db_histories = self.history_repo.get_active_participations(user_id)
            
            histories = []
            for db_history in db_histories:
                history = VolunteerHistory(
                    id=db_history.id,
                    user_id=db_history.user_id,
                    event_id=db_history.event_id,
                    participation_date=db_history.participation_date,
                    hours_volunteered=db_history.hours_volunteered,
                    status=db_history.status,
                    created_at=db_history.created_at
                )
                histories.append(history)
            
            return histories
            
        except Exception as e:
            logger.error(f"Error getting active participations: {e}")
            raise
    
    def get_stats(self, user_id: str) -> Dict[str, Any]:
        """Get volunteer statistics for a user (alias for get_user_stats)"""
        try:
            # Get user's participation history
            participations = self.get_user_history(user_id)
            
            # Calculate stats based on participation status
            total_events = len(participations)
            completed_events = len([p for p in participations if p.status == "completed"])
            pending_events = len([p for p in participations if p.status == "pending"])
            cancelled_events = len([p for p in participations if p.status == "cancelled"])
            no_show_events = len([p for p in participations if p.status == "no_show"])
            
            # Calculate completion rate
            completion_rate = (completed_events / total_events * 100) if total_events > 0 else 0.0
            
            return {
                "volunteer_id": user_id,
                "total_events": total_events,
                "completed_events": completed_events,
                "pending_events": pending_events,
                "cancelled_events": cancelled_events,
                "no_show_events": no_show_events,
                "completion_rate": completion_rate
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            # Return default stats if there's an error
            return {
                "volunteer_id": user_id,
                "total_events": 0,
                "completed_events": 0,
                "pending_events": 0,
                "cancelled_events": 0,
                "no_show_events": 0,
                "completion_rate": 0.0
            } 