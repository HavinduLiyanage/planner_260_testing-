"""
CSI3105 Testing Case Study - Equivalence Partitioning Tests
Author: Test Team
Description: Black-box testing using WEAK ROBUST equivalence partitioning criteria

WEAK ROBUST Testing Approach:
- One test case from EACH valid equivalence class
- One test case for EACH invalid equivalence class (one invalid at a time)
- All other inputs remain valid when testing one invalid input
"""

import pytest
from logic.Calendar import Calendar
from logic.Meeting import Meeting
from logic.Person import Person
from logic.Room import Room
from logic.Organization import Organization
from logic.ConflictException import ConflictsException
from tests.conftest import create_meeting


@pytest.mark.ep
class TestCalendarAddMeetingEP:
    """
    Equivalence Partitioning tests for Calendar.add_meeting()
    
    Valid ECs: month (1-12), day (1-31), start (0-23), end (0-23), start <= end
    Invalid ECs: month < 1, month > 12, day < 1, day > 31, start < 0, start >= 23, end > 23, start > end
    """
    
    def test_add_meeting_all_valid_inputs(self, valid_calendar):
        """Test with all valid equivalence classes - should succeed."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        # Verify meeting was added
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_description() == "Test Meeting"
    
    def test_add_meeting_invalid_month_below_range(self, valid_calendar):
        """Test invalid month < 1 (all other inputs valid) - should fail."""
        meeting = create_meeting(month=0, day=15, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Month does not exist"):
            valid_calendar.add_meeting(meeting)
    
    @pytest.mark.xfail(reason="BUG-003: Month 12 incorrectly rejected due to >= instead of >")
    def test_add_meeting_invalid_month_above_range(self, valid_calendar):
        """Test invalid month > 12 (all other inputs valid) - should fail."""
        meeting = create_meeting(month=13, day=15, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Month does not exist"):
            valid_calendar.add_meeting(meeting)
    
    def test_add_meeting_invalid_day_below_range(self, valid_calendar):
        """Test invalid day < 1 (all other inputs valid) - should fail."""
        meeting = create_meeting(month=6, day=0, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Day does not exist"):
            valid_calendar.add_meeting(meeting)
    
    @pytest.mark.xfail(reason="BUG-002: Day 31 universally rejected due to day > 30 check")
    def test_add_meeting_invalid_day_above_range(self, valid_calendar):
        """Test invalid day > 31 (all other inputs valid) - should fail."""
        meeting = create_meeting(month=6, day=32, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Day does not exist"):
            valid_calendar.add_meeting(meeting)
    
    def test_add_meeting_invalid_start_below_range(self, valid_calendar):
        """Test invalid start < 0 (all other inputs valid) - should fail."""
        meeting = create_meeting(month=6, day=15, start=-1, end=12)
        
        with pytest.raises(ConflictsException, match="Illegal hour"):
            valid_calendar.add_meeting(meeting)
    
    @pytest.mark.xfail(reason="BUG-004: Hour 23 incorrectly rejected due to >= instead of >")
    def test_add_meeting_invalid_start_at_boundary(self, valid_calendar):
        """Test start time = 23 (should be valid but is rejected) - BUG."""
        meeting = create_meeting(month=6, day=15, start=23, end=23)
        
        # This should NOT raise an exception, but it does due to bug
        valid_calendar.add_meeting(meeting)
    
    def test_add_meeting_invalid_end_above_range(self, valid_calendar):
        """Test invalid end > 23 (all other inputs valid) - should fail."""
        meeting = create_meeting(month=6, day=15, start=10, end=24)
        
        with pytest.raises(ConflictsException, match="Illegal hour"):
            valid_calendar.add_meeting(meeting)
    
    def test_add_meeting_invalid_start_after_end(self, valid_calendar):
        """Test invalid scenario where start > end - should fail."""
        meeting = create_meeting(month=6, day=15, start=15, end=10)
        
        with pytest.raises(ConflictsException, match="Meeting starts before it ends"):
            valid_calendar.add_meeting(meeting)
    
    def test_add_meeting_conflict_detection(self, valid_calendar):
        """Test scheduling conflict - should detect and raise exception."""
        # Add first meeting
        meeting1 = create_meeting(month=6, day=15, start=10, end=12, description="First Meeting")
        valid_calendar.add_meeting(meeting1)
        
        # Try to add overlapping meeting
        meeting2 = create_meeting(month=6, day=15, start=11, end=13, description="Second Meeting")
        
        with pytest.raises(ConflictsException, match="Overlap with another item"):
            valid_calendar.add_meeting(meeting2)


@pytest.mark.ep
class TestPersonAvailabilityEP:
    """
    Equivalence Partitioning tests for Person.is_busy()
    
    Tests the same equivalence classes as Calendar but through Person interface
    """
    
    def test_person_is_busy_all_valid_inputs(self, valid_person):
        """Test is_busy with all valid inputs - should return False."""
        # Person has no meetings yet
        result = valid_person.is_busy(month=6, day=15, start=10, end=12)
        assert result is False
    
    def test_person_is_busy_with_meeting(self, valid_person):
        """Test is_busy when person has meeting - should return True."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_person.add_meeting(meeting)
        
        # Check if busy during meeting time
        result = valid_person.is_busy(month=6, day=15, start=10, end=12)
        assert result is True
    
    def test_person_is_busy_invalid_month(self, valid_person):
        """Test is_busy with invalid month - should raise exception."""
        with pytest.raises(ConflictsException, match="Month does not exist"):
            valid_person.is_busy(month=0, day=15, start=10, end=12)
    
    @pytest.mark.xfail(reason="BUG-002: Day 31 universally rejected")
    def test_person_is_busy_invalid_day(self, valid_person):
        """Test is_busy with invalid day > 31 - should raise exception."""
        with pytest.raises(ConflictsException, match="Day does not exist"):
            valid_person.is_busy(month=6, day=32, start=10, end=12)


@pytest.mark.ep
class TestRoomAvailabilityEP:
    """
    Equivalence Partitioning tests for Room.is_busy()
    
    Tests the same equivalence classes as Calendar but through Room interface
    """
    
    def test_room_is_busy_all_valid_inputs(self, valid_room):
        """Test is_busy with all valid inputs - should return False."""
        result = valid_room.is_busy(month=6, day=15, start=10, end=12)
        assert result is False
    
    def test_room_is_busy_with_meeting(self, valid_room):
        """Test is_busy when room has meeting - should return True."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_room.add_meeting(meeting)
        
        result = valid_room.is_busy(month=6, day=15, start=10, end=12)
        assert result is True
    
    def test_room_is_busy_invalid_hour(self, valid_room):
        """Test is_busy with invalid start hour - should raise exception."""
        with pytest.raises(ConflictsException, match="Illegal hour"):
            valid_room.is_busy(month=6, day=15, start=-1, end=12)


@pytest.mark.ep
class TestOrganizationGettersEP:
    """
    Equivalence Partitioning tests for Organization.get_room() and get_employee()
    
    Valid EC: existing room/person name
    Invalid EC: non-existent name, case mismatch
    """
    
    def test_get_room_valid_existing_room(self, valid_organization):
        """Test getting an existing room - should succeed."""
        room = valid_organization.get_room("ML5.123")
        assert room.get_id() == "ML5.123"
    
    def test_get_room_invalid_non_existent(self, valid_organization):
        """Test getting non-existent room - should raise exception."""
        with pytest.raises(Exception, match="Requested room does not exist"):
            valid_organization.get_room("INVALID.ROOM")
    
    @pytest.mark.xfail(reason="BUG-007: Case sensitivity - exact match required")
    def test_get_room_case_insensitive(self, valid_organization):
        """Test getting room with different case - should work but doesn't (BUG)."""
        # ML5.123 exists, but ml5.123 should also work
        room = valid_organization.get_room("ml5.123")
        assert room.get_id() == "ML5.123"
    
    def test_get_employee_valid_existing_person(self, valid_organization):
        """Test getting an existing employee - should succeed."""
        person = valid_organization.get_employee("Justin Gardener")
        assert person.get_name() == "Justin Gardener"
    
    def test_get_employee_invalid_non_existent(self, valid_organization):
        """Test getting non-existent employee - should raise exception."""
        with pytest.raises(Exception, match="Requested employee does not exist"):
            valid_organization.get_employee("Invalid Person")
    
    @pytest.mark.xfail(reason="BUG-007: Case sensitivity - exact match required")
    def test_get_employee_case_insensitive(self, valid_organization):
        """Test getting employee with different case - should work but doesn't (BUG)."""
        # "Justin Gardener" exists
        person = valid_organization.get_employee("justin gardener")
        assert person.get_name() == "Justin Gardener"


@pytest.mark.ep
class TestMeetingCreationEP:
    """
    Equivalence Partitioning tests for Meeting object creation
    
    Valid EC: All parameters within valid ranges
    Invalid EC: Not applicable (Meeting doesn't validate, Calendar does)
    """
    
    def test_meeting_creation_all_valid(self):
        """Test creating meeting with all valid parameters."""
        room = Room("TEST.ROOM")
        person = Person("Test Person")
        
        meeting = Meeting(
            month=6,
            day=15,
            start=10,
            end=12,
            attendees=[person],
            room=room,
            description="Test Meeting"
        )
        
        assert meeting.get_month() == 6
        assert meeting.get_day() == 15
        assert meeting.get_start_time() == 10
        assert meeting.get_end_time() == 12
        assert len(meeting.get_attendees()) == 1
        assert meeting.get_room().get_id() == "TEST.ROOM"
        assert meeting.get_description() == "Test Meeting"
    
    def test_meeting_with_empty_attendees(self):
        """Test creating meeting with no attendees."""
        room = Room("TEST.ROOM")
        
        meeting = Meeting(
            month=6,
            day=15,
            start=10,
            end=12,
            attendees=[],
            room=room,
            description="Meeting with no attendees"
        )
        
        assert len(meeting.get_attendees()) == 0
    
    def test_meeting_add_remove_attendee(self):
        """Test adding and removing attendees from meeting."""
        meeting = create_meeting()
        person = Person("New Attendee")
        
        initial_count = len(meeting.get_attendees())
        meeting.add_attendee(person)
        assert len(meeting.get_attendees()) == initial_count + 1
        
        meeting.remove_attendee(person)
        assert len(meeting.get_attendees()) == initial_count
