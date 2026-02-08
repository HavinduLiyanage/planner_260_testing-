"""
CSI3105 Testing Case Study - Boundary Value Analysis Tests
Author: Test Team
Description: Black-box testing using Boundary Value Analysis (BVA)

Tests boundary values for:
- Months: 0, 1, 2, 11, 12, 13
- Days: 0, 1, 28, 29, 30, 31, 32 (varies by month)
- Hours: -1, 0, 1, 22, 23, 24
- Special cases: Feb 29 leap/non-leap, Nov 30, late evening bookings
"""

import pytest
from logic.Calendar import Calendar
from logic.Meeting import Meeting
from logic.Person import Person
from logic.Room import Room
from logic.ConflictException import ConflictsException
from tests.conftest import create_meeting


@pytest.mark.bva
class TestMonthBoundaries:
    """Test boundary values for month parameter (1-12)."""
    
    def test_month_below_minimum(self, valid_calendar):
        """Test month = 0 (below valid range) - should fail."""
        meeting = create_meeting(month=0, day=15, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Month does not exist"):
            valid_calendar.add_meeting(meeting)
    
    def test_month_at_minimum(self, valid_calendar):
        """Test month = 1 (minimum boundary) - should succeed."""
        meeting = create_meeting(month=1, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(1, 15, 0)
        assert retrieved.get_month() == 1
    
    def test_month_just_above_minimum(self, valid_calendar):
        """Test month = 2 (just above minimum) - should succeed."""
        meeting = create_meeting(month=2, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(2, 15, 0)
        assert retrieved.get_month() == 2
    
    def test_month_just_below_maximum(self, valid_calendar):
        """Test month = 11 (just below maximum) - should succeed."""
        meeting = create_meeting(month=11, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(11, 15, 0)
        assert retrieved.get_month() == 11
    
    @pytest.mark.xfail(reason="BUG-003: Month 12 rejected due to m_month >= 12 check")
    def test_month_at_maximum(self, valid_calendar):
        """Test month = 12 (maximum boundary) - should succeed but fails (BUG)."""
        meeting = create_meeting(month=12, day=15, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(12, 15, 0)
        assert retrieved.get_month() == 12
    
    def test_month_above_maximum(self, valid_calendar):
        """Test month = 13 (above valid range) - should fail."""
        meeting = create_meeting(month=13, day=15, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Month does not exist"):
            valid_calendar.add_meeting(meeting)


@pytest.mark.bva
class TestDayBoundaries:
    """Test boundary values for day parameter (varies by month)."""
    
    def test_day_below_minimum(self, valid_calendar):
        """Test day = 0 (below valid range) - should fail."""
        meeting = create_meeting(month=6, day=0, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Day does not exist"):
            valid_calendar.add_meeting(meeting)
    
    def test_day_at_minimum(self, valid_calendar):
        """Test day = 1 (minimum boundary) - should succeed."""
        meeting = create_meeting(month=6, day=1, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 1, 0)
        assert retrieved.get_day() == 1
    
    def test_day_28_february_non_leap(self, valid_calendar):
        """Test day = 28 in February (boundary for Feb) - should succeed."""
        meeting = create_meeting(month=2, day=28, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(2, 28, 0)
        assert retrieved.get_day() == 28
    
    @pytest.mark.xfail(reason="BUG-001: Feb 29 blocked even in leap years")
    def test_day_29_february_leap_year_2024(self, valid_calendar):
        """Test day = 29 in February (leap year boundary) - should succeed but fails (BUG)."""
        meeting = create_meeting(month=2, day=29, start=10, end=12)
        
        # This should work for leap year 2024 but is blocked
        valid_calendar.add_meeting(meeting)
        retrieved = valid_calendar.get_meeting(2, 29, 0)
        assert retrieved.get_day() == 29
    
    def test_day_29_30day_month(self, valid_calendar):
        """Test day = 29 in 30-day month (June) - should succeed."""
        meeting = create_meeting(month=6, day=29, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 29, 0)
        assert retrieved.get_day() == 29
    
    def test_day_30_in_30day_month(self, valid_calendar):
        """Test day = 30 in 30-day month (June) - should succeed."""
        meeting = create_meeting(month=6, day=30, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 30, 0)
        assert retrieved.get_day() == 30
    
    @pytest.mark.xfail(reason="BUG-006: November 30 incorrectly marked as non-existent")
    def test_day_30_november(self, valid_calendar):
        """Test day = 30 in November - should succeed but fails (BUG)."""
        meeting = create_meeting(month=11, day=30, start=10, end=12)
        
        # November has 30 days, but it's blocked
        valid_calendar.add_meeting(meeting)
        retrieved = valid_calendar.get_meeting(11, 30, 0)
        assert retrieved.get_day() == 30
    
    def test_day_30_in_31day_month(self, valid_calendar):
        """Test day = 30 in 31-day month (January) - should succeed."""
        meeting = create_meeting(month=1, day=30, start=10, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(1, 30, 0)
        assert retrieved.get_day() == 30
    
    @pytest.mark.xfail(reason="BUG-002: Day 31 universally rejected due to day > 30 check")
    def test_day_31_in_31day_month(self, valid_calendar):
        """Test day = 31 in 31-day month (January) - should succeed but fails (BUG)."""
        meeting = create_meeting(month=1, day=31, start=10, end=12)
        
        # January has 31 days, but day 31 is rejected
        valid_calendar.add_meeting(meeting)
        retrieved = valid_calendar.get_meeting(1, 31, 0)
        assert retrieved.get_day() == 31
    
    @pytest.mark.xfail(reason="BUG-002: Day 31 universally rejected")
    def test_day_31_in_30day_month(self, valid_calendar):
        """Test day = 31 in 30-day month (June) - should fail but for different reason."""
        meeting = create_meeting(month=6, day=31, start=10, end=12)
        
        # Should fail because June has only 30 days, but fails with wrong error
        with pytest.raises(ConflictsException, match="Day does not exist"):
            valid_calendar.add_meeting(meeting)
    
    def test_day_above_maximum(self, valid_calendar):
        """Test day = 32 (above any valid month) - should fail."""
        meeting = create_meeting(month=6, day=32, start=10, end=12)
        
        with pytest.raises(ConflictsException, match="Day does not exist"):
            valid_calendar.add_meeting(meeting)


@pytest.mark.bva
class TestHourBoundaries:
    """Test boundary values for hour parameters (0-23)."""
    
    def test_start_hour_below_minimum(self, valid_calendar):
        """Test start = -1 (below valid range) - should fail."""
        meeting = create_meeting(month=6, day=15, start=-1, end=12)
        
        with pytest.raises(ConflictsException, match="Illegal hour"):
            valid_calendar.add_meeting(meeting)
    
    def test_start_hour_at_minimum(self, valid_calendar):
        """Test start = 0 (minimum boundary) - should succeed."""
        meeting = create_meeting(month=6, day=15, start=0, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_start_time() == 0
    
    def test_start_hour_just_above_minimum(self, valid_calendar):
        """Test start = 1 (just above minimum) - should succeed."""
        meeting = create_meeting(month=6, day=15, start=1, end=12)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_start_time() == 1
    
    def test_start_hour_just_below_maximum(self, valid_calendar):
        """Test start = 22 (just below maximum) - should succeed."""
        meeting = create_meeting(month=6, day=15, start=22, end=23)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_start_time() == 22
    
    @pytest.mark.xfail(reason="BUG-004: Hour 23 rejected due to m_start >= 23 check")
    def test_start_hour_at_maximum(self, valid_calendar):
        """Test start = 23 (maximum boundary) - should succeed but fails (BUG)."""
        meeting = create_meeting(month=6, day=15, start=23, end=23)
        
        # Hour 23 (11 PM) should be valid but is rejected
        valid_calendar.add_meeting(meeting)
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_start_time() == 23
    
    def test_start_hour_above_maximum(self, valid_calendar):
        """Test start = 24 (above valid range) - should fail."""
        meeting = create_meeting(month=6, day=15, start=24, end=24)
        
        with pytest.raises(ConflictsException, match="Illegal hour"):
            valid_calendar.add_meeting(meeting)
    
    def test_end_hour_at_minimum(self, valid_calendar):
        """Test end = 0 (minimum boundary) - should succeed with start = 0."""
        meeting = create_meeting(month=6, day=15, start=0, end=0)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_end_time() == 0
    
    def test_end_hour_just_below_maximum(self, valid_calendar):
        """Test end = 22 - should succeed."""
        meeting = create_meeting(month=6, day=15, start=10, end=22)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_end_time() == 22
    
    def test_end_hour_at_maximum(self, valid_calendar):
        """Test end = 23 (maximum boundary) - should succeed."""
        meeting = create_meeting(month=6, day=15, start=10, end=23)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_end_time() == 23
    
    def test_end_hour_above_maximum(self, valid_calendar):
        """Test end = 24 (above valid range) - should fail."""
        meeting = create_meeting(month=6, day=15, start=10, end=24)
        
        with pytest.raises(ConflictsException, match="Illegal hour"):
            valid_calendar.add_meeting(meeting)


@pytest.mark.bva
class TestSpecialDateTimeCombinations:
    """Test special combinations that expose known bugs."""
    
    @pytest.mark.xfail(reason="BUG-001: Feb 29 blocked in leap years")
    def test_february_29_leap_year_2024(self, valid_calendar):
        """Test scheduling on Feb 29, 2024 (leap year) - should work but fails."""
        meeting = create_meeting(month=2, day=29, start=10, end=12,
                                description="Leap Year Meeting")
        
        # 2024 is a leap year, Feb 29 should be valid
        valid_calendar.add_meeting(meeting)
        assert valid_calendar.get_meeting(2, 29, 0) is not None
    
    @pytest.mark.xfail(reason="BUG-006: Nov 30 incorrectly blocked")
    def test_november_30(self, valid_calendar):
        """Test scheduling on November 30 - should work but fails."""
        meeting = create_meeting(month=11, day=30, start=10, end=12,
                                description="November 30 Meeting")
        
        # November has 30 days, so this should be valid
        valid_calendar.add_meeting(meeting)
        assert valid_calendar.get_meeting(11, 30, 0) is not None
    
    def test_meeting_22_to_23(self, valid_calendar):
        """Test scheduling 22:00 to 23:00 - should succeed."""
        meeting = create_meeting(month=6, day=15, start=22, end=23,
                                description="Late Evening Meeting")
        
        valid_calendar.add_meeting(meeting)
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_start_time() == 22
        assert retrieved.get_end_time() == 23
    
    @pytest.mark.xfail(reason="BUG-004: Hour 23 rejected")
    def test_meeting_23_to_23(self, valid_calendar):
        """Test scheduling 23:00 to 23:00 (1-hour slot at 11 PM) - should work but fails."""
        meeting = create_meeting(month=6, day=15, start=23, end=23,
                                description="11 PM Meeting")
        
        # This should be valid but is rejected
        valid_calendar.add_meeting(meeting)
        assert valid_calendar.get_meeting(6, 15, 0) is not None


@pytest.mark.bva
class TestStringBoundaries:
    """Test boundary values for string inputs (room/person names)."""
    
    def test_empty_room_name(self):
        """Test creating room with empty string - allowed but not ideal."""
        room = Room("")
        assert room.get_id() == ""
    
    def test_very_long_room_name(self):
        """Test creating room with very long name."""
        long_name = "A" * 100
        room = Room(long_name)
        assert room.get_id() == long_name
    
    def test_empty_person_name(self):
        """Test creating person with empty string - allowed but not ideal."""
        person = Person("")
        assert person.get_name() == ""
    
    def test_very_long_person_name(self):
        """Test creating person with very long name."""
        long_name = "B" * 100
        person = Person(long_name)
        assert person.get_name() == long_name
    
    @pytest.mark.xfail(reason="BUG-007: Exact case match required")
    def test_room_name_case_variation_lowercase(self, valid_organization):
        """Test getting room with lowercase variation - should work but doesn't."""
        # ML5.123 exists in organization
        room = valid_organization.get_room("ml5.123")
        assert room is not None
    
    @pytest.mark.xfail(reason="BUG-007: Exact case match required")
    def test_room_name_case_variation_mixed(self, valid_organization):
        """Test getting room with mixed case - should work but doesn't."""
        room = valid_organization.get_room("Ml5.123")
        assert room is not None
    
    @pytest.mark.xfail(reason="BUG-007: Exact case match required")
    def test_person_name_case_variation(self, valid_organization):
        """Test getting person with different case - should work but doesn't."""
        # "Justin Gardener" exists
        person = valid_organization.get_employee("JUSTIN GARDENER")
        assert person is not None


@pytest.mark.bva
class TestEdgeCaseScheduling:
    """Test edge cases in scheduling logic."""
    
    def test_same_start_and_end_time(self, valid_calendar):
        """Test meeting where start == end (1-hour instant meeting)."""
        meeting = create_meeting(month=6, day=15, start=10, end=10)
        valid_calendar.add_meeting(meeting)
        
        retrieved = valid_calendar.get_meeting(6, 15, 0)
        assert retrieved.get_start_time() == retrieved.get_end_time()
    
    def test_back_to_back_meetings_no_conflict(self, valid_calendar):
        """Test scheduling back-to-back meetings (should work)."""
        meeting1 = create_meeting(month=6, day=15, start=10, end=12,
                                 description="First Meeting")
        meeting2 = create_meeting(month=6, day=15, start=13, end=15,
                                 description="Second Meeting")
        
        valid_calendar.add_meeting(meeting1)
        valid_calendar.add_meeting(meeting2)
        
        assert len(valid_calendar.occupied[6][15]) == 2
    
    def test_multiple_meetings_same_day(self, valid_calendar):
        """Test scheduling multiple non-overlapping meetings on same day."""
        meetings = [
            create_meeting(month=6, day=15, start=8, end=10, description="Morning"),
            create_meeting(month=6, day=15, start=11, end=13, description="Midday"),
            create_meeting(month=6, day=15, start=14, end=16, description="Afternoon"),
        ]
        
        for meeting in meetings:
            valid_calendar.add_meeting(meeting)
        
        assert len(valid_calendar.occupied[6][15]) == 3
