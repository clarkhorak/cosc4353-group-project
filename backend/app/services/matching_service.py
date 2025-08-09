from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from app.models.matching import EventSignup
from app.utils.exceptions import ValidationError
from app.repositories.profile_repository import ProfileRepository
from app.repositories.event_repository import EventRepository
from app.repositories.history_repository import HistoryRepository
from app.repositories.user_repository import UserRepository

class MatchingService:
    def __init__(self):
        self.signups: List[EventSignup] = []
        self.profile_repo = ProfileRepository()
        self.event_repo = EventRepository()
        self.history_repo = HistoryRepository()
        self.user_repo = UserRepository()

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

    async def auto_match_volunteers(self, event_id: int) -> List[Dict[str, Any]]:
        """Match volunteers to an event using skills, availability and simple location check.

        Scoring weights:
        - skills: 0.6
        - availability (same date): 0.3
        - location proximity (city included in event.location): 0.1
        """
        # Resolve hashed numeric event_id to DB event
        db_event = self._resolve_event_by_hashed_id(event_id)
        if db_event is None:
            raise ValidationError("Event not found")

        # Parse event required skills
        try:
            event_required_skills = json.loads(db_event.required_skills) if db_event.required_skills else []
        except Exception:
            event_required_skills = []

        event_required_skills = [s.strip() for s in event_required_skills if isinstance(s, str)]
        event_date = (db_event.event_date or "").strip()
        event_location = (db_event.location or "").lower()

        # Fetch all profiles
        profiles = self.profile_repo.get_all()

        matches: List[Dict[str, Any]] = []
        for p in profiles:
            # Exclude volunteers already recorded as participated for this event
            existing = self.history_repo.get_by_user_and_event(p.user_id, db_event.id)
            if existing:
                continue

            # Parse profile skills and availability
            try:
                profile_skills = json.loads(p.skills) if p.skills else []
            except Exception:
                profile_skills = []
            try:
                profile_availability = json.loads(p.availability) if p.availability else []
            except Exception:
                profile_availability = []

            profile_skills = [s.strip() for s in profile_skills if isinstance(s, str)]

            # Compute skill score
            if event_required_skills:
                matched_skills = [s for s in profile_skills if s in event_required_skills]
                skill_score = len(matched_skills) / max(len(event_required_skills), 1)
            else:
                matched_skills = []
                skill_score = 1.0  # no requirements

            # Availability: any slot with same date
            is_available = any(
                isinstance(a, dict) and a.get("date") == event_date
                for a in profile_availability
            )
            availability_score = 1.0 if is_available else 0.0

            # Location proximity: if city string is found in event location
            city = (p.city or "").lower()
            location_score = 1.0 if city and city in event_location else 0.0

            score = 0.6 * skill_score + 0.3 * availability_score + 0.1 * location_score

            if score <= 0.0:
                continue  # skip non-matches

            user = self.user_repo.get_by_id(p.user_id)
            matches.append({
                "volunteer_id": p.user_id,
                "volunteer_email": getattr(user, "email", None),
                "volunteer_name": getattr(user, "full_name", None),
                "score": round(score, 4),
                "matched_skills": matched_skills,
                "missing_skills": [s for s in event_required_skills if s not in profile_skills],
                "available_on_date": is_available,
                "city_match": bool(location_score),
            })

        # Sort by score descending
        matches.sort(key=lambda m: m["score"], reverse=True)
        return matches

    def _resolve_event_by_hashed_id(self, hashed_id: int) -> Optional[Any]:
        for e in self.event_repo.get_all():
            try:
                if hash(e.id) % 1000000 == hashed_id:
                    return e
            except Exception:
                continue
        return None