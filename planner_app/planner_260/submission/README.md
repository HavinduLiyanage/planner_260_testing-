# Software Testing Assignment Submission

This folder contains the testing artifacts for the Scheduler Application.

## Contents

### 1. Test Suite (`tests/`)

- **Black-Box Testing**
  - `test_blackbox_ep.py`: Equivalence Partitioning tests for date/time validation (Weak Robust criteria).
  - `test_blackbox_bva.py`: Boundary Value Analysis for numeric inputs.

- **White-Box Testing (Statement Coverage)**
  - `test_whitebox_calendar.py`: 100% statement coverage for Calendar class.
  - `test_whitebox_room.py`: 100% statement coverage for Room class.
  - `test_whitebox_person.py`: 100% statement coverage for Person class.

### 2. Control Flow Graphs (`cfg_diagrams/`)

- `planner_cfg.md`: Control Flow Graphs for the Planner class (main logic).
- `calendar_cfg.md`: Control Flow Graphs for the Calendar class.
- `room_cfg.md`: Control Flow Graphs for the Room class.
- `person_cfg.md`: Control Flow Graphs for the Person class.

## Running Tests

To execute the tests, run the following command from the project root:

```bash
pytest submission/tests
```

Or to run specific categories:

```bash
# Run only black-box tests
pytest submission/tests/test_blackbox_*.py

# Run only white-box tests
pytest submission/tests/test_whitebox_*.py
```
