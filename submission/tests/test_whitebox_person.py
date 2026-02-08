"""
White-Box Statement Coverage Tests for Person Class

Goal: Achieve 100% statement coverage for all Person class methods.

The Person class is very similar to Room class - both delegate to Calendar.
We need to test all methods and ensure every code path is executed.
"""

import pytest
from logic.Person import Person
from logic.Meeting import Meeting
from logic.ConflictException import ConflictsException


class TestPersonInit:
    """Test Person initialization"""
    
    def test_person_init_with_name(self):
        """Person should initialize with provided name"""
        person = Person("Justin Gardener")
        
        assert person.name == "Justin Gardener"
        assert person.calendar is not None
    
    def test_person_init_default(self):
        """Person should initialize with empty string if no name provided"""
        person = Person()
        
        assert person.name == ""
        assert person.calendar is not None


class TestPersonGetName:
    """Test get_name() method"""
    
    def test_get_name_returns_person_name(self):
        """get_name should return the person's name"""
        person = Person("Ashley Matthews")
        
        assert person.get_name() == "Ashley Matthews"


class TestPersonAddMeeting:
    """Test add_meeting() method"""
    
    def test_add_meeting_success(self):
        """Adding meeting to available person should succeed"""
        person = Person("Justin Gardener")
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        
        # Should not raise exception
        person.add_meeting(meeting)
        
        # Verify meeting was added to calendar
        assert len(person.calendar.occupied[6][15]) == 1
    
    def test_add_meeting_conflict_raises_exception_with_person_info(self):
        """Conflicting meeting should raise exception with person name"""
        person = Person("Justin Gardener")
        
        # Add first meeting
        meeting1 = Meeting(6, 15, 10, 12, description="First Meeting")
        person.add_meeting(meeting1)
        
        # Try to add conflicting meeting
        meeting2 = Meeting(6, 15, 11, 13, description="Second Meeting")
        
        with pytest.raises(ConflictsException) as exc_info:
            person.add_meeting(meeting2)
        
        # Exception message should include person name
        assert "Justin Gardener" in str(exc_info.value)
        assert "Conflict for attendee" in str(exc_info.value)


class TestPersonPrintAgenda:
    """Test print_agenda() method"""
    
    def test_print_agenda_month_only(self):
        """print_agenda with month only should delegate to calendar"""
        person = Person("Justin Gardener")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        person.add_meeting(meeting)
        
        # Get agenda for month
        agenda = person.print_agenda(6)
        
        # Should contain meeting info
        assert "Team Meeting" in agenda
    
    def test_print_agenda_with_day(self):
        """print_agenda with month and day should delegate to calendar"""
        person = Person("Justin Gardener")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        person.add_meeting(meeting)
        
        # Get agenda for specific day
        agenda = person.print_agenda(6, 15)
        
        # Should contain meeting info
        assert "Team Meeting" in agenda
    
    def test_print_agenda_empty(self):
        """print_agenda for person with no meetings should return no meetings message"""
        person = Person("Justin Gardener")
        
        agenda = person.print_agenda(6, 15)
        
        assert "No Meetings" in agenda


class TestPersonIsBusy:
    """Test is_busy() method"""
    
    def test_is_busy_returns_false_when_free(self):
        """is_busy should return False when person is free"""
        person = Person("Justin Gardener")
        
        # Person should be free initially
        assert person.is_busy(6, 15, 10, 12) == False
    
    def test_is_busy_returns_true_when_occupied(self):
        """is_busy should return True when person is busy"""
        person = Person("Justin Gardener")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        person.add_meeting(meeting)
        
        # Person should be busy during that time
        assert person.is_busy(6, 15, 11, 13) == True
    
    def test_is_busy_validates_inputs(self):
        """is_busy should raise exception for invalid inputs"""
        person = Person("Justin Gardener")
        
        with pytest.raises(ConflictsException):
            person.is_busy(6, 32, 10, 12)  # Invalid day


class TestPersonGetMeeting:
    """Test get_meeting() method"""
    
    def test_get_meeting_returns_correct_meeting(self):
        """get_meeting should return the meeting at specified index"""
        person = Person("Justin Gardener")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        person.add_meeting(meeting)
        
        # Get the meeting
        retrieved = person.get_meeting(6, 15, 0)
        
        assert retrieved == meeting


class TestPersonRemoveMeeting:
    """Test remove_meeting() method"""
    
    def test_remove_meeting_deletes_meeting(self):
        """remove_meeting should delete the meeting"""
        person = Person("Justin Gardener")
        
        # Add meeting
        meeting = Meeting(6, 15, 10, 12, description="Team Meeting")
        person.add_meeting(meeting)
        
        # Verify it's there
        assert len(person.calendar.occupied[6][15]) == 1
        
        # Remove it
        person.remove_meeting(6, 15, 0)
        
        # Verify it's gone
        assert len(person.calendar.occupied[6][15]) == 0
