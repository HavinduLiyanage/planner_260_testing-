"""
Equivalence Partitioning Tests for Date/Time Input Validation
Using Weak Robust Testing Criteria

This test module validates the Calendar.check_times() method using EP.
According to the assignment, we use weak robust criteria which means:
- One valid value from each valid equivalence class
- One invalid value from each invalid equivalence class
"""

import pytest
from logic.Calendar import Calendar
from logic.ConflictException import ConflictsException


class TestEPDateTimeValidation:
    """
    Equivalence Partitioning tests for Calendar.check_times()
    
    Valid Equivalence Classes:
    - Month: 1-12
    - Day: 1-30 (based on check_times implementation)
    - Start Hour: 0-22 (based on check_times implementation)  
    - End Hour: 0-23
    - Start < End
    
    Invalid Equivalence Classes:
    - Month < 1
    - Month > 12 (actually >= 12 based on bug in line 65)
    - Day < 1
    - Day > 30
    - Start Hour < 0
    - Start Hour >= 23 (bug in line 67)
    - End Hour < 0
    - End Hour > 23
    - Start > End
    """
    
    def test_valid_date_time_ep(self):
        """
        EP Test Case 1: Valid inputs from each valid equivalence class
        Expected: No exception raised
        """
        # Valid: month=6, day=15, start=10, end=12
        try:
            Calendar.check_times(6, 15, 10, 12)
            assert True  # Should pass without exception
        except ConflictsException:
            pytest.fail("Valid inputs should not raise ConflictsException")
    
    def test_invalid_month_too_low_ep(self):
        """
        EP Test Case 2: Invalid month < 1
        Expected: ConflictsException with "Month does not exist"
        """
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(0, 15,10, 12)
    
    def test_invalid_month_too_high_ep(self):
        """
        EP Test Case 3: Invalid month >= 12 (BUG: should be > 12)
        Expected: ConflictsException
        
        NOTE: Line 65 has bug - uses '>=' instead of '>'
        This means month=12 (December) is incorrectly rejected!
        """
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(13, 15, 10, 12)
    
    def test_invalid_day_too_low_ep(self):
        """
        EP Test Case 4: Invalid day < 1
        Expected: ConflictsException with "Day does not exist"
        """
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 0, 10, 12)
    
    def test_invalid_day_too_high_ep(self):
        """
        EP Test Case 5: Invalid day > 30
        Expected: ConflictsException with "Day does not exist"
        
        NOTE: Line 63 restricts day to max 30, which is correct for April, June,
        September, November, but causes issues for months with 31 days.
        This is a known bug - November 30 should be valid but gets blocked.
        """
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 31, 10, 12)
    
    def test_invalid_start_hour_too_low_ep(self):
        """
        EP Test Case 6: Invalid start hour < 0
        Expected: ConflictsException with "Illegal hour"
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, -1, 12)
    
    def test_invalid_start_hour_too_high_ep(self):
        """
        EP Test Case 7: Invalid start hour >= 23 (BUG: should be > 23)
        Expected: ConflictsException with "Illegal hour"
        
        NOTE: Line 67 has bug - uses '>=' instead of '>'
        This means start hour 23 (11 PM) is incorrectly rejected!
        This is the documented 11 PM booking bug.
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 24, 12)
    
    def test_invalid_end_hour_too_low_ep(self):
        """
        EP Test Case 8: Invalid end hour < 0
        Expected: ConflictsException with "Illegal hour"
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 10, -1)
    
    def test_invalid_end_hour_too_high_ep(self):
        """
        EP Test Case 9: Invalid end hour > 23
        Expected: ConflictsException with "Illegal hour"
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 10, 24)
    
    def test_invalid_start_after_end_ep(self):
        """
        EP Test Case 10: Start time > End time (logical error)
        Expected: ConflictsException with "Meeting starts before it ends"
        """
        with pytest.raises(ConflictsException, match="Meeting starts before it ends"):
            Calendar.check_times(6, 15, 14, 10)


class TestEPBugRepro:
    """
    Additional EP tests to specifically reproduce documented bugs
    """
    
    def test_december_month_bug_ep(self):
        """
        BUG REPRODUCTION: December (month=12) incorrectly rejected
        Line 65 uses m_month >= 12 instead of > 12
        Expected: Should be valid, but raises exception
        """
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(12, 15, 10, 12)
    
    def test_november_30_bug_ep(self):
        """
        BUG REPRODUCTION: November 30 incorrectly rejected
        Line 63 uses m_day > 30 instead of proper month-specific validation
        Expected: Should be valid (Nov has 30 days), but raises exception
        """
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(11, 30, 10, 12)
    
    def test_start_hour_23_bug_ep(self):
        """
        BUG REPRODUCTION: Start hour 23 (11 PM) incorrectly rejected
        Line 67 uses m_start >= 23 instead of > 23
        Expected: Should be valid, but raises exception
        This is the documented 11 PM - 11:59 PM booking bug
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 23, 23)
    
    def test_day_31_for_valid_months_ep(self):
        """
        BUG REPRODUCTION: Day 31 rejected for all months
        Line 63 blocks day 31 for ALL months, even those with 31 days
        Expected: Should be valid for Jan, Mar, May, Jul, Aug, Oct, Dec but raises exception
        """
        # January has 31 days, should be valid
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(1, 31, 10, 12)
