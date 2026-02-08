# Comprehensive Test Case Catalog

This document provides a detailed list of all 108 test cases implemented for the Planner application.

## 1. Equivalence Partitioning (EP) Tests
**File:** `test_blackbox_ep.py` (14 cases)
**Target:** `Calendar.check_times()`

| Test Case | Description / Validation Logic |
|-----------|--------------------------------|
| `test_valid_date_time_ep` | Valid inputs from each valid equivalence class. Expects no exception. |
| `test_invalid_month_too_low_ep` | Month < 1. Expects "Month does not exist". |
| `test_invalid_month_too_high_ep` | Month > 12 (targets BUG: month=12 rejection). Expects "Month does not exist". |
| `test_invalid_day_too_low_ep` | Day < 1. Expects "Day does not exist". |
| `test_invalid_day_too_high_ep` | Day > 30 (targets BUG: 31st day rejection). Expects "Day does not exist". |
| `test_invalid_start_hour_too_low_ep` | Start hour < 0. Expects "Illegal hour". |
| `test_invalid_start_hour_too_high_ep` | Start hour >= 23 (targets BUG: 11 PM rejection). Expects "Illegal hour". |
| `test_invalid_end_hour_too_low_ep` | End hour < 0. Expects "Illegal hour". |
| `test_invalid_end_hour_too_high_ep` | End hour > 23. Expects "Illegal hour". |
| `test_invalid_start_after_end_ep` | Start > End error. Expects "Meeting starts before it ends". |
| `test_december_month_bug_ep` | Specifically reproduces the December month rejection bug. |
| `test_november_30_bug_ep` | Verifies the pre-blocking bug where Nov 30 is incorrectly marked as non-existent. |
| `test_start_hour_23_bug_ep` | Specifically reproduces the 11 PM booking failure. |
| `test_day_31_for_valid_months_ep` | Reproduces the bug where the 31st is rejected for all months. |

---

## 2. Boundary Value Analysis (BVA) Tests
**File:** `test_blackbox_bva.py` (35 cases)
**Target:** `Calendar.check_times()` and special date boundaries.

### Month Boundaries (7 cases)
- `test_month_min_minus_1`: Month = 0 (Invalid)
- `test_month_min`: Month = 1 (Valid)
- `test_month_min_plus_1`: Month = 2 (Valid)
- `test_month_nominal`: Month = 6 (Valid)
- `test_month_max_minus_1`: Month = 11 (Valid)
- `test_month_max`: Month = 12 (Targeting Bug: Invalid)
- `test_month_max_plus_1`: Month = 13 (Invalid)

### Day Boundaries (8 cases)
- `test_day_min_minus_1`: Day = 0 (Invalid)
- `test_day_min`: Day = 1 (Valid)
- `test_day_min_plus_1`: Day = 2 (Valid)
- `test_day_nominal`: Day = 15 (Valid)
- `test_day_max_minus_1`: Day = 29 (Valid)
- `test_day_30`: Day = 30 (Valid)
- `test_day_max_plus_1`: Day = 31 (Targeting Bug: Invalid)
- `test_day_32`: Day = 32 (Invalid)

### Hour Boundaries (14 cases)
- **Start Hour:** -1, 0, 1, 12, 22, 23 (Bug), 24.
- **End Hour:** -1, 0, 1, 12, 22, 23, 24.

### Special Cases (6 cases)
- `test_february_29_boundary`: Checks if Feb 29 passes `check_times`.
- `test_november_30_boundary`: Checks if Nov 30 passes `check_times`.
- `test_april_30_boundary`: Checks if April 30 passes `check_times`.
- `test_january_31_boundary`: Verifies Jan 31 rejection bug.
- `test_11pm_to_1159pm_booking`: Verifies 11 PM start hour failure.
- `test_vacation_day_32_boundary`: Verifies day 32 rejection.

---

## 3. White-Box Tests (Calendar)
**File:** `test_whitebox_calendar.py` (33 cases)
**Objective:** Statement Coverage for `Calendar` class.

| Category | Cases |
|----------|-------|
| **Initialization** | `creates_structure`, `blocks_feb_29_30_31`, `blocks_invalid_month_days` |
| **Availability** | `is_busy_empty_slot`, `is_busy_occupied_start_overlap`, `is_busy_occupied_end_overlap`, `is_busy_validates_inputs` |
| **Validation** | 10 cases covering all branches of `check_times` (min/max/logical errors). |
| **Persistence** | `add_meeting_success`, `add_meeting_validates_inputs`, `add_meeting_creates_missing_month`, `add_meeting_creates_missing_day`, `add_meeting_conflict_start_overlap`, `add_meeting_conflict_end_overlap`, `add_meeting_to_blocked_date` |
| **Management** | `clear_schedule_removes_meetings`, `get_meeting_returns_correct_meeting`, `get_meeting_invalid_index_raises_error`, `remove_meeting_deletes_meeting`, `remove_meeting_invalid_index_raises_error` |
| **Agenda UI** | `print_agenda_month_empty`, `print_agenda_month_with_meetings`, `print_agenda_day_empty`, `print_agenda_day_with_meetings` |

---

## 4. White-Box Tests (Person)
**File:** `test_whitebox_person.py` (13 cases)
**Objective:** Statement Coverage for `Person` class.

- `test_person_init_with_name`: Custom name init.
- `test_person_init_default`: Empty name init.
- `test_get_name_returns_person_name`: Name retrieval.
- `test_add_meeting_success`: Adding meeting.
- `test_add_meeting_conflict_raises_exception_with_person_info`: Verifies name in exception string.
- `test_print_agenda_month_only`: Monthly agenda delegation.
- `test_print_agenda_with_day`: Daily agenda delegation.
- `test_print_agenda_empty`: Empty agenda message.
- `test_is_busy_returns_false_when_free`: Free state.
- `test_is_busy_returns_true_when_occupied`: Busy state.
- `test_is_busy_validates_inputs`: Exception on invalid inputs.
- `test_get_meeting_returns_correct_meeting`: Meeting retrieval.
- `test_remove_meeting_deletes_meeting`: Meeting removal.

---

## 5. White-Box Tests (Room)
**File:** `test_whitebox_room.py` (13 cases)
**Objective:** Statement Coverage for `Room` class.

- `test_room_init_with_id`: Room ID init.
- `test_room_init_default`: Empty ID init.
- `test_get_id_returns_room_id`: ID retrieval.
- `test_add_meeting_success`: Successful booking.
- `test_add_meeting_conflict_raises_exception_with_room_info`: Verifies Room ID in exception string.
- `test_print_agenda_month_only`: Monthly agenda delegation.
- `test_print_agenda_with_day`: Daily agenda delegation.
- `test_print_agenda_empty`: Empty agenda message.
- `test_is_busy_returns_false_when_free`: Free state.
- `test_is_busy_returns_true_when_occupied`: Busy state.
- `test_is_busy_validates_inputs`: Exception on invalid inputs.
- `test_get_meeting_returns_correct_meeting`: Meeting retrieval index.
- `test_remove_meeting_deletes_meeting`: Meeting removal index.
