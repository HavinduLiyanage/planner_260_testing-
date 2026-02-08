"""
White-Box Statement Coverage Tests for Room Class

Goal: Achieve 100% statement coverage for all Room class methods.

The Room class delegates most logic to its internal Calendar object.
We need to test all methods and ensure every code path is executed.
"""

import pytest
from logic.Room import Room
from logic.Meeting import Meeting
from logic.ConflictException import ConflictsException


class TestRoomInit:
    """Test Room initialization"""
    
    def test_room_init_with_id(self):
        """Room should initialize with provided ID"""
        room = Room("JO18.330")
        
        assert room.id == "JO18.330"
        assert room.calendar is not None
    
    def test_room_init_default(self):
        """Room should initialize with empty string if no ID provided"""
        room = Room()
        
        assert room.id == ""
        assert room.calendar is not None


class TestRoomGetId:
    """Test get_id() method"""
    
    def test_get_id_returns_room_id(self):
        """get_id should return the room's ID"""
        room = Room("ML5.123")
        
        assert room.get_id() == "ML5.123"


class TestRoomAddMeeting:
    """Test add_meeting() method"""
    
    def test_add_meeting_success(self):
        """Adding meeting to available room should succeed"""
        room = Room("JO18.330")
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        
        # Should not raise exception
        room.add_meeting(meeting)
        
        # Verify meeting was added to calendar
        assert len(room.calendar.occupied[6][15]) == 1
    
    def test_add_meeting_conflict_raises_exception_with_room_info(self):
        """Conflicting meeting should raise exception with room ID"""
        room = Room("JO18.330")
        
        # Add first meeting
        meeting1 = Meeting(6, 15, 10, 12, description="First Meeting")
        room.add_meeting(meeting1)
        
        # Try to add conflicting meeting
        meeting2 = Meeting(6, 15, 11, 13, description="Second Meeting")
        
        with pytest.raises(ConflictsException) as exc_info:
            room.add_meeting(meeting2)
        
        # Exception message should include room ID
        assert "JO18.330" in str(exc_info.value)
        assert "Conflict for room" in str(exc_info.value)


class TestRoomPrintAgenda:
    """Test print_agenda() method"""
    
    def test_print_agenda_month_only(self):
        """print_agenda with month only should delegate to calendar"""
        room = Room("JO18.330")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Room Booking")
        room.add_meeting(meeting)
        
        # Get agenda for month
        agenda = room.print_agenda(6)
        
        # Should contain meeting info
        assert "Room Booking" in agenda
    
    def test_print_agenda_with_day(self):
        """print_agenda with month and day should delegate to calendar"""
        room = Room("JO18.330")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Room Booking")
        room.add_meeting(meeting)
        
        # Get agenda for specific day
        agenda = room.print_agenda(6, 15)
        
        # Should contain meeting info
        assert "Room Booking" in agenda
    
    def test_print_agenda_empty(self):
        """print_agenda for empty room should return no meetings message"""
        room = Room("JO18.330")
        
        agenda = room.print_agenda(6, 15)
        
        assert "No Meetings" in agenda


class TestRoomIsBusy:
    """Test is_busy() method"""
    
    def test_is_busy_returns_false_when_free(self):
        """is_busy should return False when room is free"""
        room = Room("JO18.330")
        
        # Room should be free initially
        assert room.is_busy(6, 15, 10, 12) == False
    
    def test_is_busy_returns_true_when_occupied(self):
        """is_busy should return True when room is occupied"""
        room = Room("JO18.330")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Room Booking")
        room.add_meeting(meeting)
        
        # Room should be busy during that time
        assert room.is_busy(6, 15, 11, 13) == True
    
    def test_is_busy_validates_inputs(self):
        """is_busy should raise exception for invalid inputs"""
        room = Room("JO18.330")
        
        with pytest.raises(ConflictsException):
            room.is_busy(6, 32, 10, 12)  # Invalid day


class TestRoomGetMeeting:
    """Test get_meeting() method"""
    
    def test_get_meeting_returns_correct_meeting(self):
        """get_meeting should return the meeting at specified index"""
        room = Room("JO18.330")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Room Booking")
        room.add_meeting(meeting)
        
        # Get the meeting
        retrieved = room.get_meeting(6, 15, 0)
        
        assert retrieved == meeting


class TestRoomRemoveMeeting:
    """Test remove_meeting() method"""
    
    def test_remove_meeting_deletes_meeting(self):
        """remove_meeting should delete the meeting"""
        room = Room("JO18.330")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Room Booking")
        room.add_meeting(meeting)
        
        # Verify it's there
        assert len(room.calendar.occupied[6][15]) == 1
        
        # Remove it
        room.remove_meeting(6, 15, 0)
        
        # Verify it's gone
        assert len(room.calendar.occupied[6][15]) == 0
