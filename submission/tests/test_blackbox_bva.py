"""
Boundary Value Analysis Tests for Date/Time Input Validation

This test module applies BVA to all numeric inputs (month, day, start hour, end hour).
BVA tests the boundaries: min-1, min, min+1, nominal, max-1, max, max+1

According to requirements, this helps verify the known bugs:
- Feb 29 leap year issue
- 11 PM booking issue
- Nov 30 issue
- Day 31/32 issues
"""

import pytest
from logic.Calendar import Calendar
from logic.ConflictException import ConflictsException


class TestBVAMonth:
    """Boundary Value Analysis for Month parameter"""
    
    def test_month_min_minus_1(self):
        """BVA: Month = 0 (min-1) - Invalid"""
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(0, 15, 10, 12)
    
    def test_month_min(self):
        """BVA: Month = 1 (min) - Valid (January)"""
        try:
            Calendar.check_times(1, 15, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Month 1 (January) should be valid")
    
    def test_month_min_plus_1(self):
        """BVA: Month = 2 (min+1) - Valid (February)"""
        try:
            Calendar.check_times(2, 15, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Month 2 (February) should be valid")
    
    def test_month_nominal(self):
        """BVA: Month = 6 (nominal) - Valid (June)"""
        try:
            Calendar.check_times(6, 15, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Month 6 (June) should be valid")
    
    def test_month_max_minus_1(self):
        """BVA: Month = 11 (max-1) - Valid (November)"""
        try:
            Calendar.check_times(11, 15, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Month 11 (November) should be valid")
    
    def test_month_max(self):
        """
        BVA: Month = 12 (max) - Should be valid (December)
        BUG: Line 65 uses >= 12 instead of > 12, so December is rejected!
        """
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(12, 15, 10, 12)
    
    def test_month_max_plus_1(self):
        """BVA: Month = 13 (max+1) - Invalid"""
        with pytest.raises(ConflictsException, match="Month does not exist"):
            Calendar.check_times(13, 15, 10, 12)


class TestBVADay:
    """Boundary Value Analysis for Day parameter"""
    
    def test_day_min_minus_1(self):
        """BVA: Day = 0 (min-1) - Invalid"""
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 0, 10, 12)
    
    def test_day_min(self):
        """BVA: Day = 1 (min) - Valid"""
        try:
            Calendar.check_times(6, 1, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Day 1 should be valid")
    
    def test_day_min_plus_1(self):
        """BVA: Day = 2 (min+1) - Valid"""
        try:
            Calendar.check_times(6, 2, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Day 2 should be valid")
    
    def test_day_nominal(self):
        """BVA: Day = 15 (nominal) - Valid"""
        try:
            Calendar.check_times(6, 15, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Day 15 should be valid")
    
    def test_day_max_minus_1(self):
        """BVA: Day = 29 (near max) - Valid for most months"""
        try:
            Calendar.check_times(6, 29, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Day 29 should be valid for most months")
    
    def test_day_30(self):
        """
        BVA: Day = 30 - Valid for most months
        Code allows day 30, but check implementation in __init__ for November
        """
        try:
            Calendar.check_times(6, 30, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Day 30 should be valid")
    
    def test_day_max_plus_1(self):
        """
        BVA: Day = 31 (max for some months)
        BUG: Line 63 rejects day > 30, so day 31 is always invalid
        even for months that have 31 days (Jan, Mar, May, Jul, Aug, Oct, Dec)
        """
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(1, 31, 10, 12)  # January should allow day 31
    
    def test_day_32(self):
        """BVA: Day = 32 (max+2) - Always invalid"""
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 32, 10, 12)


class TestBVAStartHour:
    """Boundary Value Analysis for Start Hour parameter"""
    
    def test_start_hour_min_minus_1(self):
        """BVA: Start = -1 (min-1) - Invalid"""
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, -1, 12)
    
    def test_start_hour_min(self):
        """BVA: Start = 0 (min) - Valid (midnight)"""
        try:
            Calendar.check_times(6, 15, 0, 12)
            assert True
        except ConflictsException:
            pytest.fail("Start hour 0 (midnight) should be valid")
    
    def test_start_hour_min_plus_1(self):
        """BVA: Start = 1 (min+1) - Valid"""
        try:
            Calendar.check_times(6, 15, 1, 12)
            assert True
        except ConflictsException:
            pytest.fail("Start hour 1 should be valid")
    
    def test_start_hour_nominal(self):
        """BVA: Start = 12 (nominal) - Valid (noon)"""
        try:
            Calendar.check_times(6, 15, 12, 15)
            assert True
        except ConflictsException:
            pytest.fail("Start hour 12 (noon) should be valid")
    
    def test_start_hour_max_minus_1(self):
        """BVA: Start = 22 (max-1) - Valid"""
        try:
            Calendar.check_times(6, 15, 22, 23)
            assert True
        except ConflictsException:
            pytest.fail("Start hour 22 should be valid")
    
    def test_start_hour_max(self):
        """
        BVA: Start = 23 (max) - Should be valid (11 PM)
        BUG: Line 67 uses >= 23 instead of > 23, so hour 23 is rejected!
        This is the documented 11 PM - 11:59 PM booking bug
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 23, 23)
    
    def test_start_hour_max_plus_1(self):
        """BVA: Start = 24 (max+1) - Invalid"""
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 24, 23)


class TestBVAEndHour:
    """Boundary Value Analysis for End Hour parameter"""
    
    def test_end_hour_min_minus_1(self):
        """BVA: End = -1 (min-1) - Invalid"""
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 10, -1)
    
    def test_end_hour_min(self):
        """BVA: End = 0 (min) - Valid if start <= 0"""
        try:
            Calendar.check_times(6, 15, 0, 0)
            assert True
        except ConflictsException:
            pytest.fail("End hour 0 should be valid when start is 0")
    
    def test_end_hour_min_plus_1(self):
        """BVA: End = 1 (min+1) - Valid"""
        try:
            Calendar.check_times(6, 15, 0, 1)
            assert True
        except ConflictsException:
            pytest.fail("End hour 1 should be valid when start <= 1")
    
    def test_end_hour_nominal(self):
        """BVA: End = 12 (nominal) - Valid (noon)"""
        try:
            Calendar.check_times(6, 15, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("End hour 12 should be valid")
    
    def test_end_hour_max_minus_1(self):
        """BVA: End = 22 (max-1) - Valid"""
        try:
            Calendar.check_times(6, 15, 20, 22)
            assert True
        except ConflictsException:
            pytest.fail("End hour 22 should be valid")
    
    def test_end_hour_max(self):
        """BVA: End = 23 (max) - Valid (11 PM)"""
        try:
            Calendar.check_times(6, 15, 20, 23)
            assert True
        except ConflictsException:
            pytest.fail("End hour 23 should be valid")
    
    def test_end_hour_max_plus_1(self):
        """BVA: End = 24 (max+1) - Invalid"""
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 10, 24)


class TestBVASpecialCases:
    """BVA tests for special date cases mentioned in requirements"""
    
    def test_february_29_boundary(self):
        """
        BVA Special Case: February 29
        Assignment mentions Feb 29 leap year bug.
        
        The check_times method blocks day > 30, so Feb 29 passes validation.
        However, Calendar.__init__ pre-blocks Feb 29 with a "Day does not exist" meeting.
        This test only checks check_times validation, not Calendar.add_meeting.
        """
        try:
            Calendar.check_times(2, 29, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("Feb 29 should pass check_times validation")
    
    def test_november_30_boundary(self):
        """
        BVA Special Case: November 30
        Assignment mentions Nov 30 booking failure.
        
        November has 30 days, so Nov 30 should be valid.
        However, Calendar.__init__ (line 28) blocks Nov 30 AND 31 incorrectly!
        This test only checks check_times validation.
        """
        try:
            Calendar.check_times(11, 30, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("November 30 should pass check_times validation")
    
    def test_april_30_boundary(self):
        """BVA Special Case: April 30 (valid - April has 30 days)"""
        try:
            Calendar.check_times(4, 30, 10, 12)
            assert True
        except ConflictsException:
            pytest.fail("April 30 should be valid")
    
    def test_january_31_boundary(self):
        """
        BVA Special Case: January 31
        BUG: January has 31 days, but check_times rejects day > 30
        """
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(1, 31, 10, 12)
    
    def test_11pm_to_1159pm_booking(self):
        """
        BVA Special Case: 11 PM to 11:59 PM booking
        Assignment mentions events between 11:00 PM - 11:59 PM fail.
        
        BUG: Line 67 uses m_start >= 23, so start hour 23 is rejected
        """
        with pytest.raises(ConflictsException, match="Illegal hour"):
            Calendar.check_times(6, 15, 23, 23)
    
    def test_vacation_day_32_boundary(self):
        """
        BVA Special Case: Day 32
        Assignment mentions vacation can be booked with day 32.
        check_times correctly rejects day > 30, so day 32 should fail.
        (The vacation bug might be elsewhere in the system)
        """
        with pytest.raises(ConflictsException, match="Day does not exist"):
            Calendar.check_times(6, 32, 10, 12)
