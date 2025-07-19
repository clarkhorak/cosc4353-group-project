import pytest
from datetime import datetime, date, time
from app.services.history_service import HistoryService
from app.models.history import ParticipationStatus, VolunteerHistory, VolunteerStats

@pytest.fixture
def history_service():
    return HistoryService()

@pytest.mark.asyncio
async def test_participate_success(history_service):
    """Test successful participation in an event"""
    user_id = "user1"
    event_id = 1
    
    result = await history_service.participate(user_id, event_id)
    
    assert result.volunteer_id == user_id
    assert result.event_id == event_id
    assert result.status == ParticipationStatus.PENDING
    assert result.event_name == "Community Cleanup"
    assert result.joined_at is not None

@pytest.mark.asyncio
async def test_participate_duplicate(history_service):
    """Test that duplicate participation is prevented"""
    user_id = "user1"
    event_id = 1
    
    # First participation should succeed
    await history_service.participate(user_id, event_id)
    
    # Second participation should fail
    with pytest.raises(Exception, match="Already participating"):
        await history_service.participate(user_id, event_id)

@pytest.mark.asyncio
async def test_update_status_success(history_service):
    """Test successful status update"""
    user_id = "user1"
    event_id = 1
    
    # First participate
    await history_service.participate(user_id, event_id)
    
    # Then update status
    result = await history_service.update_status(user_id, event_id, ParticipationStatus.COMPLETED)
    
    assert result.status == ParticipationStatus.COMPLETED

@pytest.mark.asyncio
async def test_update_status_not_found(history_service):
    """Test status update for non-existent participation"""
    user_id = "user1"
    event_id = 1
    
    with pytest.raises(Exception, match="Participation not found"):
        await history_service.update_status(user_id, event_id, ParticipationStatus.COMPLETED)

@pytest.mark.asyncio
async def test_get_history_empty(history_service):
    """Test getting history for user with no participations"""
    user_id = "user1"
    
    result = await history_service.get_history(user_id)
    
    assert result == []

@pytest.mark.asyncio
async def test_get_history_with_participations(history_service):
    """Test getting history for user with participations"""
    user_id = "user1"
    event_id1 = 1
    event_id2 = 2
    
    # Add participations
    await history_service.participate(user_id, event_id1)
    await history_service.participate(user_id, event_id2)
    
    result = await history_service.get_history(user_id)
    
    assert len(result) == 2
    assert result[0].event_id == event_id1
    assert result[1].event_id == event_id2

@pytest.mark.asyncio
async def test_get_stats_empty(history_service):
    """Test getting stats for user with no participations"""
    user_id = "user1"
    
    result = await history_service.get_stats(user_id)
    
    assert result.total_events == 0
    assert result.completion_rate == 0.0
    assert result.completed_events == 0
    assert result.pending_events == 0

@pytest.mark.asyncio
async def test_get_stats_with_completed_events(history_service):
    """Test getting stats for user with completed events"""
    user_id = "user1"
    event_id = 1
    
    # Participate and complete
    await history_service.participate(user_id, event_id)
    await history_service.update_status(user_id, event_id, ParticipationStatus.COMPLETED)
    
    result = await history_service.get_stats(user_id)
    
    assert result.total_events == 1
    assert result.completion_rate == 1.0
    assert result.completed_events == 1
    assert result.pending_events == 0

@pytest.mark.asyncio
async def test_get_stats_partial_completion(history_service):
    """Test getting stats for user with mixed completion status"""
    user_id = "user1"
    event_id1 = 1
    event_id2 = 2
    
    # Complete first event
    await history_service.participate(user_id, event_id1)
    await history_service.update_status(user_id, event_id1, ParticipationStatus.COMPLETED)
    
    # Leave second event pending
    await history_service.participate(user_id, event_id2)
    
    result = await history_service.get_stats(user_id)
    
    assert result.total_events == 2
    assert result.completion_rate == 0.5
    assert result.completed_events == 1
    assert result.pending_events == 1 