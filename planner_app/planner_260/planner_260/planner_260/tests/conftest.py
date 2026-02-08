"""
CSI3105 Testing Case Study - Test Fixtures and Utilities
Author: Test Team
Description: Shared fixtures and helper functions for all test modules
"""

import pytest
from logic.Calendar import Calendar
from logic.Meeting import Meeting
from logic.Person import Person
from logic.Room import Room
from logic.Organization import Organization


@pytest.fixture
def valid_calendar():
    """Returns a fresh Calendar instance for testing."""
    return Calendar()


@pytest.fixture
def valid_organization():
    """Returns an Organization instance with predefined employees and rooms."""
    return Organization()


@pytest.fixture
def valid_room():
    """Returns a test Room object."""
    return Room("TEST.ROOM.101")


@pytest.fixture
def valid_person():
    """Returns a test Person object."""
    return Person("Test Person")


@pytest.fixture
def sample_meeting():
    """Returns a valid Meeting object for testing."""
    room = Room("ML5.123")
    person1 = Person("Alice")
    person2 = Person("Bob")
    
    meeting = Meeting(
        month=6,
        day=15,
        start=10,
        end=12,
        attendees=[person1, person2],
        room=room,
        description="Sample Test Meeting"
    )
    return meeting


@pytest.fixture
def calendar_with_meeting(valid_calendar, sample_meeting):
    """Returns a Calendar with one meeting already scheduled."""
    valid_calendar.add_meeting(sample_meeting)
    return valid_calendar


# Helper functions for creating test data

def create_meeting(month=6, day=15, start=10, end=12, description="Test Meeting"):
    """
    Helper function to create a Meeting object with default or custom parameters.
    
    Args:
        month: Month of meeting (1-12)
        day: Day of meeting (1-31)
        start: Start hour (0-23)
        end: End hour (0-23)
        description: Meeting description
    
    Returns:
        Meeting object
    """
    room = Room("TEST.ROOM")
    person = Person("Test Attendee")
    
    return Meeting(
        month=month,
        day=day,
        start=start,
        end=end,
        attendees=[person],
        room=room,
        description=description
    )


def is_leap_year(year):
    """
    Check if a year is a leap year.
    
    Args:
        year: The year to check
    
    Returns:
        True if leap year, False otherwise
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# Constants for testing

# Valid test values
VALID_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
VALID_DAYS_31 = list(range(1, 32))  # For months with 31 days
VALID_DAYS_30 = list(range(1, 31))  # For months with 30 days
VALID_DAYS_FEB = list(range(1, 29))  # For February (non-leap)
VALID_HOURS = list(range(0, 24))

# Months with different day counts
MONTHS_WITH_31_DAYS = [1, 3, 5, 7, 8, 10, 12]
MONTHS_WITH_30_DAYS = [4, 6, 9, 11]

# Boundary values for testing
MONTH_BOUNDARIES = [0, 1, 2, 11, 12, 13]
DAY_BOUNDARIES = [0, 1, 28, 29, 30, 31, 32]
HOUR_BOUNDARIES = [-1, 0, 1, 22, 23, 24]

# Test room and person names
TEST_ROOMS = ["ML5.123", "JO18.330", "JO7.221", "TEST.ROOM"]
TEST_PERSONS = ["Justin Gardener", "Ashley Martin", "Test Person"]
