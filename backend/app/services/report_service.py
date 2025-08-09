from __future__ import annotations

from typing import List, Dict, Any

from app.repositories.user_repository import UserRepository
from app.repositories.event_repository import EventRepository
from app.repositories.history_repository import HistoryRepository


class ReportService:
    """
    Service for generating datasets used for admin reports.

    This service aggregates data from multiple repositories to produce
    flattened, report-friendly rows. File/format rendering (CSV/PDF)
    is handled at the API layer.
    """

    def __init__(self) -> None:
        self.user_repo = UserRepository()
        self.event_repo = EventRepository()
        self.history_repo = HistoryRepository()

    def get_volunteer_history_rows(self) -> List[Dict[str, Any]]:
        """
        Returns one row per volunteer participation (based on History).

        Columns:
        - volunteer_id, volunteer_email, volunteer_full_name
        - event_id, event_title, participation_date, hours_volunteered, status
        """
        users = {u.id: u for u in self.user_repo.get_all(skip=0, limit=10_000)}
        events = {e.id: e for e in self.event_repo.get_all(skip=0, limit=10_000)}
        histories = self.history_repo.get_all(skip=0, limit=100_000)

        rows: List[Dict[str, Any]] = []
        for h in histories:
            user = users.get(h.user_id)
            event = events.get(h.event_id)
            rows.append(
                {
                    "volunteer_id": h.user_id,
                    "volunteer_email": getattr(user, "email", None),
                    "volunteer_full_name": getattr(user, "full_name", None),
                    "event_id": h.event_id,
                    "event_title": getattr(event, "title", None),
                    "participation_date": h.participation_date,
                    "hours_volunteered": h.hours_volunteered,
                    "status": h.status,
                }
            )
        return rows

    def get_event_assignment_rows(self) -> List[Dict[str, Any]]:
        """
        Returns event details with volunteer assignments based on History.

        One row per event per volunteer (if none, a single row with volunteer columns empty).

        Columns:
        - event_id, title, category, date, start_time, end_time, location,
          capacity, status, urgency
        - volunteer_id, volunteer_email, volunteer_full_name, hours_volunteered, participation_status
        """
        users = {u.id: u for u in self.user_repo.get_all(skip=0, limit=10_000)}
        events = self.event_repo.get_all(skip=0, limit=10_000)
        event_id_to_event = {e.id: e for e in events}

        rows: List[Dict[str, Any]] = []
        # Build mapping from event_id to histories
        histories = self.history_repo.get_all(skip=0, limit=100_000)
        event_to_histories: Dict[str, List[Any]] = {}
        for h in histories:
            event_to_histories.setdefault(h.event_id, []).append(h)

        for event in events:
            histories_for_event = event_to_histories.get(event.id, [])
            if not histories_for_event:
                rows.append(
                    {
                        "event_id": event.id,
                        "title": event.title,
                        "category": event.category,
                        "event_date": event.event_date,
                        "start_time": event.start_time,
                        "end_time": event.end_time,
                        "location": event.location,
                        "capacity": event.capacity,
                        "status": event.status,
                        "urgency": event.urgency,
                        "volunteer_id": None,
                        "volunteer_email": None,
                        "volunteer_full_name": None,
                        "hours_volunteered": None,
                        "participation_status": None,
                    }
                )
                continue

            for h in histories_for_event:
                user = users.get(h.user_id)
                rows.append(
                    {
                        "event_id": event.id,
                        "title": event.title,
                        "category": event.category,
                        "event_date": event.event_date,
                        "start_time": event.start_time,
                        "end_time": event.end_time,
                        "location": event.location,
                        "capacity": event.capacity,
                        "status": event.status,
                        "urgency": event.urgency,
                        "volunteer_id": h.user_id,
                        "volunteer_email": getattr(user, "email", None),
                        "volunteer_full_name": getattr(user, "full_name", None),
                        "hours_volunteered": h.hours_volunteered,
                        "participation_status": h.status,
                    }
                )

        return rows


