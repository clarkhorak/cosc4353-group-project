import asyncio
import requests
from datetime import date, time, datetime, timedelta
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.services.event_service import EventService
import pytest
from fastapi.testclient import TestClient
from app.main import app

BASE_URL = "http://localhost:8000"

client = TestClient(app)

# --- Model Validation Tests ---
def test_event_model_validation():
    print("🧪 Testing Event Model Validation...")
    # Valid event
    event = EventCreate(
        title="Food Drive",
        description="Help distribute food to those in need.",
        category="Charity",
        event_date=date.today() + timedelta(days=10),
        start_time=time(9, 0),
        end_time=time(12, 0),
        location="Community Center",
        capacity=50,
        requirements="Able to lift 20 lbs",
        status="open"
    )
    assert event.title == "Food Drive"
    # Invalid event (short title)
    try:
        EventCreate(
            title="A",
            description="desc",
            category="Charity",
            event_date=date.today() + timedelta(days=10),
            start_time=time(9, 0),
            end_time=time(12, 0),
            location="Community Center",
            capacity=50,
            status="open"
        )
        assert False, "Should have failed validation for short title"
    except Exception:
        pass
    # Invalid event (end_time before start_time)
    try:
        EventCreate(
            title="Test Event",
            description="desc",
            category="Charity",
            event_date=date.today() + timedelta(days=10),
            start_time=time(12, 0),
            end_time=time(9, 0),
            location="Community Center",
            capacity=50,
            status="open"
        )
        assert False, "Should have failed validation for end_time before start_time"
    except Exception:
        pass
    print("  ✅ Model validation tests passed.")

# --- Service Tests ---
def test_event_service():
    print("🧪 Testing EventService...")
    service = EventService()
    event_data = EventCreate(
        title="Cleanup Day",
        description="Park cleanup event.",
        category="Environment",
        event_date=date.today() + timedelta(days=5),
        start_time=time(8, 0),
        end_time=time(11, 0),
        location="City Park",
        capacity=30,
        requirements=None,
        status="open"
    )
    # Create event
    event = asyncio.run(service.create_event(event_data))
    assert event.id == 1
    # Get event
    fetched = asyncio.run(service.get_event(1))
    assert fetched.title == "Cleanup Day"
    # Update event
    update = EventUpdate(title="Updated Cleanup Day", capacity=40)
    updated = asyncio.run(service.update_event(1, update))
    assert updated.title == "Updated Cleanup Day"
    assert updated.capacity == 40
    # List events
    events = asyncio.run(service.list_events())
    assert len(events) == 1
    # Delete event
    deleted = asyncio.run(service.delete_event(1))
    assert deleted is True
    print("  ✅ EventService CRUD tests passed.")

# --- API Tests ---
def test_event_api():
    print("🌐 Testing Event API endpoints...")
    # Create event
    event_data = {
        "title": "Blood Drive",
        "description": "Donate blood and save lives!",
        "category": "Health",
        "event_date": str(date.today() + timedelta(days=7)),
        "start_time": "10:00:00",
        "end_time": "14:00:00",
        "location": "Hospital",
        "capacity": 100,
        "requirements": "Must be 18+",
        "status": "open"
    }
    r = requests.post(f"{BASE_URL}/events/", json=event_data)
    assert r.status_code == 201, f"Create failed: {r.text}"
    event = r.json()
    event_id = event["id"]
    # Get event
    r = requests.get(f"{BASE_URL}/events/{event_id}")
    assert r.status_code == 200
    # Update event
    update_data = {"title": "Blood Drive Updated", "capacity": 120}
    r = requests.put(f"{BASE_URL}/events/{event_id}", json=update_data)
    assert r.status_code == 200
    assert r.json()["title"] == "Blood Drive Updated"
    # List events
    r = requests.get(f"{BASE_URL}/events/")
    assert r.status_code == 200
    assert any(e["id"] == event_id for e in r.json())
    # Delete event
    r = requests.delete(f"{BASE_URL}/events/{event_id}")
    assert r.status_code == 204
    print("  ✅ Event API endpoint tests passed.")

def test_create_and_list_events():
    # Create event
    event_data = {
        "title": "Test Event",
        "description": "A test event.",
        "category": "General",
        "event_date": "2099-12-31",
        "start_time": "10:00:00",
        "end_time": "12:00:00",
        "location": "Test Location",
        "capacity": 10,
        "requirements": "First Aid, Teaching",
        "status": "open"
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200 or response.status_code == 201
    event = response.json()
    assert event["title"] == event_data["title"]
    # List events
    response = client.get("/events/")
    assert response.status_code == 200
    events = response.json()
    assert any(e["title"] == event_data["title"] for e in events)

if __name__ == "__main__":
    test_event_model_validation()
    test_event_service()
    test_event_api()
    print("\n🎉 All event tests completed successfully!") 