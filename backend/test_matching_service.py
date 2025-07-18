import pytest
from datetime import datetime, date, time
from app.services.matching_service import MatchingService

@pytest.fixture
def matching_service():
    return MatchingService()

@pytest.mark.asyncio
async def test_signup_for_event_success(matching_service):
    """Test successful signup for an event"""
    volunteer_id = "vol1"
    event_id = 1
    
    result = await matching_service.signup_for_event(volunteer_id, event_id)
    
    assert result.volunteer_id == volunteer_id
    assert result.event_id == event_id
    assert result.status == "pending"
    assert result.signup_time is not None

@pytest.mark.asyncio
async def test_signup_for_event_duplicate(matching_service):
    """Test that duplicate signup is prevented"""
    volunteer_id = "vol1"
    event_id = 1
    
    # First signup should succeed
    await matching_service.signup_for_event(volunteer_id, event_id)
    
    # Second signup should fail
    with pytest.raises(Exception, match="Already signed up"):
        await matching_service.signup_for_event(volunteer_id, event_id)

@pytest.mark.asyncio
async def test_signup_for_event_different_volunteers(matching_service):
    """Test that different volunteers can sign up for the same event"""
    volunteer1_id = "vol1"
    volunteer2_id = "vol2"
    event_id = 1
    
    # Both signups should succeed
    result1 = await matching_service.signup_for_event(volunteer1_id, event_id)
    result2 = await matching_service.signup_for_event(volunteer2_id, event_id)
    
    assert result1.volunteer_id == volunteer1_id
    assert result2.volunteer_id == volunteer2_id
    assert result1.event_id == event_id
    assert result2.event_id == event_id

@pytest.mark.asyncio
async def test_cancel_signup_success(matching_service):
    """Test successful signup cancellation"""
    volunteer_id = "vol1"
    event_id = 1
    
    # First signup
    await matching_service.signup_for_event(volunteer_id, event_id)
    
    # Then cancel
    result = await matching_service.cancel_signup(volunteer_id, event_id)
    
    assert result is True

@pytest.mark.asyncio
async def test_cancel_signup_not_found(matching_service):
    """Test cancellation of non-existent signup"""
    volunteer_id = "vol1"
    event_id = 1
    
    with pytest.raises(Exception, match="Signup not found"):
        await matching_service.cancel_signup(volunteer_id, event_id)

@pytest.mark.asyncio
async def test_cancel_signup_already_cancelled(matching_service):
    """Test cancellation of already cancelled signup"""
    volunteer_id = "vol1"
    event_id = 1
    
    # Signup and cancel
    await matching_service.signup_for_event(volunteer_id, event_id)
    await matching_service.cancel_signup(volunteer_id, event_id)
    
    # Try to cancel again
    with pytest.raises(Exception, match="Signup not found"):
        await matching_service.cancel_signup(volunteer_id, event_id)

@pytest.mark.asyncio
async def test_list_signups_for_event_empty(matching_service):
    """Test listing signups for event with no signups"""
    event_id = 1
    
    result = await matching_service.list_signups_for_event(event_id)
    
    assert result == []

@pytest.mark.asyncio
async def test_list_signups_for_event_with_signups(matching_service):
    """Test listing signups for event with multiple signups"""
    volunteer1_id = "vol1"
    volunteer2_id = "vol2"
    event_id = 1
    
    # Add signups
    await matching_service.signup_for_event(volunteer1_id, event_id)
    await matching_service.signup_for_event(volunteer2_id, event_id)
    
    result = await matching_service.list_signups_for_event(event_id)
    
    assert len(result) == 2
    volunteer_ids = [s.volunteer_id for s in result]
    assert volunteer1_id in volunteer_ids
    assert volunteer2_id in volunteer_ids

@pytest.mark.asyncio
async def test_list_signups_for_event_excludes_cancelled(matching_service):
    """Test that cancelled signups are excluded from event listing"""
    volunteer1_id = "vol1"
    volunteer2_id = "vol2"
    event_id = 1
    
    # Add signups
    await matching_service.signup_for_event(volunteer1_id, event_id)
    await matching_service.signup_for_event(volunteer2_id, event_id)
    
    # Cancel one signup
    await matching_service.cancel_signup(volunteer1_id, event_id)
    
    result = await matching_service.list_signups_for_event(event_id)
    
    assert len(result) == 1
    assert result[0].volunteer_id == volunteer2_id

@pytest.mark.asyncio
async def test_list_signups_for_volunteer_empty(matching_service):
    """Test listing signups for volunteer with no signups"""
    volunteer_id = "vol1"
    
    result = await matching_service.list_signups_for_volunteer(volunteer_id)
    
    assert result == []

@pytest.mark.asyncio
async def test_list_signups_for_volunteer_with_signups(matching_service):
    """Test listing signups for volunteer with multiple signups"""
    volunteer_id = "vol1"
    event1_id = 1
    event2_id = 2
    
    # Add signups
    await matching_service.signup_for_event(volunteer_id, event1_id)
    await matching_service.signup_for_event(volunteer_id, event2_id)
    
    result = await matching_service.list_signups_for_volunteer(volunteer_id)
    
    assert len(result) == 2
    event_ids = [s.event_id for s in result]
    assert event1_id in event_ids
    assert event2_id in event_ids

@pytest.mark.asyncio
async def test_list_signups_for_volunteer_excludes_cancelled(matching_service):
    """Test that cancelled signups are excluded from volunteer listing"""
    volunteer_id = "vol1"
    event1_id = 1
    event2_id = 2
    
    # Add signups
    await matching_service.signup_for_event(volunteer_id, event1_id)
    await matching_service.signup_for_event(volunteer_id, event2_id)
    
    # Cancel one signup
    await matching_service.cancel_signup(volunteer_id, event1_id)
    
    result = await matching_service.list_signups_for_volunteer(volunteer_id)
    
    assert len(result) == 1
    assert result[0].event_id == event2_id 