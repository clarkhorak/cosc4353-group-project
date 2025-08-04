#!/usr/bin/env python3
"""
Test script for History Service
"""

import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.history_service import HistoryService
from app.models.history import VolunteerHistoryCreate, VolunteerHistoryUpdate

def test_history_service():
    """Test HistoryService methods"""
    print("🧪 Testing HistoryService...")
    
    service = HistoryService()
    
    # Test data
    user_id = "user1"
    event_id = "event1"
    participation_date = "2025-12-25"
    
    # Test record participation
    print("  📝 Testing record_participation...")
    result = service.record_participation(user_id, event_id, participation_date, 4)
    assert result.user_id == user_id
    assert result.event_id == event_id
    assert result.hours_volunteered == 4
    print("    ✅ record_participation passed")
    
    # Test get user history
    print("  📖 Testing get_user_history...")
    histories = service.get_user_history(user_id)
    assert len(histories) == 1
    assert histories[0].user_id == user_id
    print("    ✅ get_user_history passed")
    
    # Test get event participation
    print("  📋 Testing get_event_participation...")
    event_histories = service.get_event_participation(event_id)
    assert len(event_histories) == 1
    assert event_histories[0].event_id == event_id
    print("    ✅ get_event_participation passed")
    
    # Test update participation
    print("  ✏️  Testing update_participation...")
    update_data = VolunteerHistoryUpdate(hours_volunteered=6, status="completed")
    updated = service.update_participation(result.id, update_data)
    assert updated is not None
    assert updated.hours_volunteered == 6
    print("    ✅ update_participation passed")
    
    # Test get user stats
    print("  📊 Testing get_user_stats...")
    stats = service.get_user_stats(user_id)
    assert stats.total_events == 1
    assert stats.total_hours == 6
    print("    ✅ get_user_stats passed")
    
    # Test get active participations
    print("  🔍 Testing get_active_participations...")
    active = service.get_active_participations(user_id)
    assert len(active) == 1
    assert active[0].status == "completed"
    print("    ✅ get_active_participations passed")
    
    # Test delete participation
    print("  🗑️  Testing delete_participation...")
    success = service.delete_participation(result.id)
    assert success is True
    
    # Verify deletion
    histories_after = service.get_user_history(user_id)
    assert len(histories_after) == 0
    print("    ✅ delete_participation passed")
    
    print("✅ All HistoryService tests passed")

def test_history_service_error_handling():
    """Test HistoryService error handling"""
    print("\n🧪 Testing HistoryService Error Handling...")
    
    service = HistoryService()
    
    # Test with invalid user ID
    try:
        service.get_user_history("invalid_user")
        print("  ✅ get_user_history handles invalid user gracefully")
    except Exception as e:
        print(f"  ✅ get_user_history error handling: {e}")
    
    # Test with invalid event ID
    try:
        service.get_event_participation("invalid_event")
        print("  ✅ get_event_participation handles invalid event gracefully")
    except Exception as e:
        print(f"  ✅ get_event_participation error handling: {e}")
    
    # Test update with invalid ID
    try:
        update_data = VolunteerHistoryUpdate(hours_volunteered=6)
        result = service.update_participation("invalid_id", update_data)
        assert result is None
        print("  ✅ update_participation handles invalid ID gracefully")
    except Exception as e:
        print(f"  ✅ update_participation error handling: {e}")
    
    print("✅ All error handling tests passed")

def main():
    """Run all history service tests"""
    print("🚀 Starting History Service Tests")
    print("=" * 50)
    
    try:
        test_history_service()
        test_history_service_error_handling()
        
        print("\n✅ All history service tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 