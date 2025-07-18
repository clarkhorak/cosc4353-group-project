import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

VOLUNTEER_ID = "vol1"
EVENT_ID = 1


def test_signup():
    print("🧪 Testing signup for event...")
    r = requests.post(f"{BASE_URL}/matching/signup", params={"volunteer_id": VOLUNTEER_ID, "event_id": EVENT_ID})
    assert r.status_code == 201, f"Signup failed: {r.text}"
    signup = r.json()
    print("  ✅ Signup successful:", signup)
    return signup

def test_list_signups_for_event():
    print("🧪 Testing list signups for event...")
    r = requests.get(f"{BASE_URL}/matching/event/{EVENT_ID}")
    assert r.status_code == 200, f"List signups for event failed: {r.text}"
    signups = r.json()
    print(f"  ✅ {len(signups)} signups found for event {EVENT_ID}")
    return signups

def test_list_signups_for_volunteer():
    print("🧪 Testing list signups for volunteer...")
    r = requests.get(f"{BASE_URL}/matching/volunteer/{VOLUNTEER_ID}")
    assert r.status_code == 200, f"List signups for volunteer failed: {r.text}"
    signups = r.json()
    print(f"  ✅ {len(signups)} signups found for volunteer {VOLUNTEER_ID}")
    return signups

def test_cancel_signup():
    print("🧪 Testing cancel signup...")
    r = requests.delete(f"{BASE_URL}/matching/signup", params={"volunteer_id": VOLUNTEER_ID, "event_id": EVENT_ID})
    assert r.status_code == 204, f"Cancel signup failed: {r.text}"
    print("  ✅ Signup cancelled successfully")

def main():
    print("\n🚀 Starting Matching API Tests\n")
    test_signup()
    test_list_signups_for_event()
    test_list_signups_for_volunteer()
    test_cancel_signup()
    print("\n🎉 All matching API tests completed successfully!")

if __name__ == "__main__":
    main() 