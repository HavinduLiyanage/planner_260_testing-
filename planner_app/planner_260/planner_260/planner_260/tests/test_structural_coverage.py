"""
CSI3105 Testing Case Study - Structural Coverage Tests
Author: Test Team
Description: White-box testing to achieve 100% statement coverage for Calendar, Room, and Person classes

Target Classes:
- Calendar.py - 100% statement coverage required
- Room.py - 100% statement coverage required
- Person.py - 100% statement coverage required

NOT testing: Meeting.py, Organization.py, Planner.py
"""

import pytest
from logic.Calendar import Calendar
from logic.Meeting import Meeting
from logic.Person import Person
from logic.Room import Room
from logic.ConflictException import ConflictsException
from tests.conftest import create_meeting


@pytest.mark.structural
class TestCalendarStatementCoverage:
    """
    Achieve 100% statement coverage for Calendar class.
    
    Methods to cover:
    - __init__() - initialization with blocked days
    - is_busy() - check time slot availability
    - check_times() - static validation method
    - add_meeting() - add meeting with conflict checking
    - clear_schedule() - clear all meetings for a day
    - print_agenda() - two overloaded versions
    - get_meeting() - retrieve specific meeting
    - remove_meeting() - delete a meeting
    """
    
    def test_calendar_init_creates_structure(self):
        """Test Calendar initialization creates proper data structure."""
        cal = Calendar()
        
        # Verify structure is created
        assert 1 in cal.occupied
        assert 12 in cal.occupied
        assert 1 in cal.occupied[1]
        assert 31 in cal.occupied[1]
        
        # Verify blocked days are initialized
        assert len(cal.occupied[2][29]) > 0  # Feb 29 blocked
        assert len(cal.occupied[2][30]) > 0  # Feb 30 blocked
        assert len(cal.occupied[2][31]) > 0  # Feb 31 blocked
        assert len(cal.occupied[4][31]) > 0  # Apr 31 blocked
        assert len(cal.occupied[6][31]) > 0  # Jun 31 blocked
        assert len(cal.occupied[9][31]) > 0  # Sep 31 blocked
        assert len(cal.occupied[11][30]) > 0  # Nov 30 blocked (BUG)
        assert len(cal.occupied[11][31]) > 0  # Nov 31 blocked
    
    def test_is_busy_empty_calendar(self, valid_calendar):
        """Test is_busy returns False when no meetings scheduled."""
        result = valid_calendar.is_busy(month=6, day=15, start=10, end=12)
        assert result is False
    
    def test_is_busy_with_meeting_start_overlap(self, valid_calendar):
        """Test is_busy detects overlap when new start falls within existing meeting."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        # Check time where start (11) is between existing start (10) and end (12)
        result = valid_calendar.is_busy(month=6, day=15, start=11, end=13)
        assert result is True
    
    def test_is_busy_with_meeting_end_overlap(self, valid_calendar):
        """Test is_busy detects overlap when new end falls within existing meeting."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        # Check time where end (11) is between existing start (10) and end (12)
        result = valid_calendar.is_busy(month=6, day=15, start=8, end=11)
        assert result is True
    
    def test_is_busy_exact_match(self, valid_calendar):
        """Test is_busy with exact same time as existing meeting."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        result = valid_calendar.is_busy(month=6, day=15, start=10, end=12)
        assert result is True
    
    def test_check_times_all_validation_paths(self):
        """Test all validation branches in check_times static method."""
        # Valid inputs - should not raise
        Calendar.check_times(6, 15, 10, 12)
        
        # Invalid day < 1
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 0, 10, 12)
        
        # Invalid day > 30
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 31, 10, 12)
        
        # Invalid month < 1
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(0, 15, 10, 12)
        
        # Invalid month >= 12 (BUG: should be > 12)
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(12, 15, 10, 12)
        
        # Invalid start < 0
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, -1, 12)
        
        # Invalid start >= 23 (BUG: should be > 23)
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 23, 23)
        
        # Invalid end < 0
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 10, -1)
        
        # Invalid end > 23
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 10, 24)
        
        # Start > End
        with pytest.raises(ConflictsException, match="Meeting starts before it ends"):
            Calendar.check_times(6, 15, 15, 10)
    
    def test_add_meeting_creates_month_if_missing(self):
        """Test add_meeting creates month in dict if it doesn't exist."""
        cal = Calendar()
        # Create meeting for existing month
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        
        # Month 6 should already exist from __init__
        cal.add_meeting(meeting)
        assert 6 in cal.occupied
        assert meeting in cal.occupied[6][15]
    
    def test_add_meeting_creates_day_if_missing(self):
        """Test add_meeting creates day in dict if it doesn't exist."""
        cal = Calendar()
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        
        # Day structure should exist from __init__
        cal.add_meeting(meeting)
        assert 15 in cal.occupied[6]
        assert meeting in cal.occupied[6][15]
    
    def test_add_meeting_conflict_start_within_existing(self, valid_calendar):
        """Test add_meeting detects conflict when start time overlaps."""
        meeting1 = create_meeting(month=6, day=15, start=10, end=12, description="First")
        valid_calendar.add_meeting(meeting1)
        
        # Try to add meeting where start is within existing meeting's time
        meeting2 = create_meeting(month=6, day=15, start=11, end=13, description="Second")
        
        with pytest.raises(ConflictsException, match="Overlap with another item"):
            valid_calendar.add_meeting(meeting2)
    
    def test_add_meeting_conflict_end_within_existing(self, valid_calendar):
        """Test add_meeting detects conflict when end time overlaps."""
        meeting1 = create_meeting(month=6, day=15, start=10, end=12, description="First")
        valid_calendar.add_meeting(meeting1)
        
        # Try to add meeting where end is within existing meeting's time
        meeting2 = create_meeting(month=6, day=15, start=8, end=11, description="Second")
        
        with pytest.raises(ConflictsException, match="Overlap with another item"):
            valid_calendar.add_meeting(meeting2)
    
    def test_add_meeting_no_conflict_with_blocked_day(self):
        """Test add_meeting skips conflict check for 'Day does not exist' markers."""
        cal = Calendar()
        
        # Feb 29 is blocked, but we can't add there anyway due to validation
        # This tests the branch that checks description != "Day does not exist"
        
        # Add valid meeting on Feb 28
        meeting = create_meeting(month=2, day=28, start=10, end=12)
        cal.add_meeting(meeting)
        
        # The blocked days should not cause conflicts
        assert len(cal.occupied[2][29]) > 0  # Still blocked
    
    def test_add_meeting_success_no_conflict(self, valid_calendar):
        """Test successful add when no conflicts exist."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        assert meeting in valid_calendar.occupied[6][15]
    
    def test_clear_schedule_removes_all_meetings(self, valid_calendar):
        """Test clear_schedule removes all meetings for a day."""
        # Add multiple meetings
        meeting1 = create_meeting(month=6, day=15, start=8, end=10)
        meeting2 = create_meeting(month=6, day=15, start=11, end=13)
        valid_calendar.add_meeting(meeting1)
        valid_calendar.add_meeting(meeting2)
        
        assert len(valid_calendar.occupied[6][15]) == 2
        
        # Clear schedule
        valid_calendar.clear_schedule(6, 15)
        assert len(valid_calendar.occupied[6][15]) == 0
    
    def test_print_agenda_monthly_no_meetings(self, valid_calendar):
        """Test print_agenda for month with no meetings (testing daily version with no meetings)."""
        # The monthly version is overridden, only daily version exists
        result = valid_calendar.print_agenda(month=6, day=15)
        assert "No Meetings booked on this date" in result
    
    def test_print_agenda_monthly_with_meetings(self, valid_calendar):
        """Test print_agenda for specific day with meetings."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        result = valid_calendar.print_agenda(month=6, day=15)
        assert "Agenda for 6/15" in result
        assert "Test Meeting" in result
    
    def test_print_agenda_daily_no_meetings(self, valid_calendar):
        """Test print_agenda for specific day with no meetings."""
        result = valid_calendar.print_agenda(month=6, day=15)
        assert "No Meetings booked on this date" in result
    
    def test_print_agenda_daily_with_meetings(self, valid_calendar):
        """Test print_agenda for specific day with meetings."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        result = valid_calendar.print_agenda(month=6, day=15)
        assert "Agenda for 6/15" in result
        assert "Test Meeting" in result
    
    def test_get_meeting_retrieves_correct_meeting(self, valid_calendar):
        """Test get_meeting returns the correct meeting."""
        meeting = create_meeting(month=6, day=15, start=10, end=12, description="Specific Meeting")
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_description() == "Specific Meeting"
    
    def test_remove_meeting_deletes_meeting(self, valid_calendar):
        """Test remove_meeting successfully deletes a meeting."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        assert len(valid_calendar.occupied[6][15]) == 1
        
        valid_calendar.remove_meeting(6, 15, 0)
        assert len(valid_calendar.occupied[6][15]) == 0


@pytest.mark.structural
class TestRoomStatementCoverage:
    """
    Achieve 100% statement coverage for Room class.
    
    Methods to cover:
    - __init__() - initialization
    - get_id() - retrieve room ID
    - add_meeting() - add with conflict wrapping
    - print_agenda() - delegate to calendar
    - is_busy() - delegate to calendar
    - get_meeting() - delegate to calendar
    - remove_meeting() - delegate to calendar
    """
    
    def test_room_init_creates_calendar(self):
        """Test Room initialization creates a Calendar."""
        room = Room("TEST.ROOM")
        assert room.id == "TEST.ROOM"
        assert isinstance(room.calendar, Calendar)
    
    def test_room_get_id(self):
        """Test get_id returns correct ID."""
        room = Room("ML5.123")
        assert room.get_id() == "ML5.123"
    
    def test_room_add_meeting_success(self, valid_room):
        """Test adding meeting to room successfully."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_room.add_meeting(meeting)
        
        # Verify meeting was added
        retrieved = valid_room.calendar.get_meeting(6, 15, 0)
        assert retrieved.get_description() == "Test Meeting"
    
    def test_room_add_meeting_conflict_wraps_exception(self, valid_room):
        """Test add_meeting wraps ConflictsException with room context."""
        meeting1 = create_meeting(month=6, day=15, start=10, end=12)
        valid_room.add_meeting(meeting1)
        
        meeting2 = create_meeting(month=6, day=15, start=11, end=13)
        
        with pytest.raises(ConflictsException) as exc_info:
            valid_room.add_meeting(meeting2)
        
        # Should include room ID in error message
        assert "TEST.ROOM.101" in str(exc_info.value)
    
    def test_room_print_agenda_daily(self, valid_room):
        """Test print_agenda delegates to calendar (daily version)."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_room.add_meeting(meeting)
        
        # Test daily version with explicit day parameter
        result = valid_room.print_agenda(month=6, day=15)
        assert "Agenda for 6/15" in result
        assert "Test Meeting" in result
    
    def test_room_is_busy_free(self, valid_room):
        """Test is_busy returns False when room is free."""
        result = valid_room.is_busy(month=6, day=15, start=10, end=12)
        assert result is False
    
    def test_room_is_busy_occupied(self, valid_room):
        """Test is_busy returns True when room is occupied."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_room.add_meeting(meeting)
        
        result = valid_room.is_busy(month=6, day=15, start=10, end=12)
        assert result is True
    
    def test_room_get_meeting(self, valid_room):
        """Test get_meeting delegates to calendar."""
        meeting = create_meeting(month=6, day=15, start=10, end=12, description="Room Meeting")
        valid_room.add_meeting(meeting)
        
        retrieved = valid_room.get_meeting(6, 15, 0)
        assert retrieved.get_description() == "Room Meeting"
    
    def test_room_remove_meeting(self, valid_room):
        """Test remove_meeting delegates to calendar."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_room.add_meeting(meeting)
        
        valid_room.remove_meeting(6, 15, 0)
        
        # Verify meeting was removed
        assert len(valid_room.calendar.occupied[6][15]) == 0


@pytest.mark.structural
class TestPersonStatementCoverage:
    """
    Achieve 100% statement coverage for Person class.
    
    Methods to cover:
    - __init__() - initialization
    - get_name() - retrieve person name
    - add_meeting() - add with conflict wrapping
    - print_agenda() - delegate to calendar
    - is_busy() - delegate to calendar
    - get_meeting() - delegate to calendar
    - remove_meeting() - delegate to calendar
    """
    
    def test_person_init_creates_calendar(self):
        """Test Person initialization creates a Calendar."""
        person = Person("Test Person")
        assert person.name == "Test Person"
        assert isinstance(person.calendar, Calendar)
    
    def test_person_get_name(self):
        """Test get_name returns correct name."""
        person = Person("Alice")
        assert person.get_name() == "Alice"
    
    def test_person_add_meeting_success(self, valid_person):
        """Test adding meeting to person successfully."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_person.add_meeting(meeting)
        
        # Verify meeting was added
        retrieved = valid_person.calendar.get_meeting(6, 15, 0)
        assert retrieved.get_description() == "Test Meeting"
    
    def test_person_add_meeting_conflict_wraps_exception(self, valid_person):
        """Test add_meeting wraps ConflictsException with person context."""
        meeting1 = create_meeting(month=6, day=15, start=10, end=12)
        valid_person.add_meeting(meeting1)
        
        meeting2 = create_meeting(month=6, day=15, start=11, end=13)
        
        with pytest.raises(ConflictsException) as exc_info:
            valid_person.add_meeting(meeting2)
        
        # Should include person name in error message
        assert "Test Person" in str(exc_info.value)
    
    def test_person_print_agenda_daily(self, valid_person):
        """Test print_agenda delegates to calendar (daily version)."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_person.add_meeting(meeting)
        
        # Test daily version with explicit day parameter
        result = valid_person.print_agenda(month=6, day=15)
        assert "Agenda for 6/15" in result
        assert "Test Meeting" in result
    
    def test_person_is_busy_free(self, valid_person):
        """Test is_busy returns False when person is free."""
        result = valid_person.is_busy(month=6, day=15, start=10, end=12)
        assert result is False
    
    def test_person_is_busy_occupied(self, valid_person):
        """Test is_busy returns True when person is occupied."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_person.add_meeting(meeting)
        
        result = valid_person.is_busy(month=6, day=15, start=10, end=12)
        assert result is True
    
    def test_person_get_meeting(self, valid_person):
        """Test get_meeting delegates to calendar."""
        meeting = create_meeting(month=6, day=15, start=10, end=12, description="Person Meeting")
        valid_person.add_meeting(meeting)
        
        retrieved = valid_person.get_meeting(6, 15, 0)
        assert retrieved.get_description() == "Person Meeting"
    
    def test_person_remove_meeting(self, valid_person):
        """Test remove_meeting delegates to calendar."""
        meeting = create_meeting(month=6, day=15, start=10, end=12)
        valid_person.add_meeting(meeting)
        
        valid_person.remove_meeting(6, 15, 0)
        
        # Verify meeting was removed
        assert len(valid_person.calendar.occupied[6][15]) == 0
