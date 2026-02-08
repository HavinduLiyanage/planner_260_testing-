# Control Flow Graph (CFG) - Calendar Class

## Overview

This document presents the Control Flow Graphs for key methods in the Calendar class. CFGs visualize the control flow through each method, showing all decision points and execution paths.

## CFG Notation

- **Rectangular nodes**: Statements/blocks of code
- **Diamond nodes**: Decision points (if/else, loops)
- **Edges**: Control flow paths
- **Node numbers**: For reference

---

## 1. Calendar.__init__() CFG

```mermaid
graph TD
    start([Start]) --> n1[Create empty occupied dict<br/>months 0-12, days 0-31]
    n1 --> n2[Import Meeting class]
    n2 --> n3[Block Feb 29:<br/>Add 'Day does not exist' meeting]
    n3 --> n4[Block Feb 30:<br/>Add 'Day does not exist' meeting]
    n4 --> n5[Block Feb 31:<br/>Add 'Day does not exist' meeting]
    n5 --> n6[Block Apr 31:<br/>Add 'Day does not exist' meeting]
    n6 --> n7[Block Jun 31:<br/>Add 'Day does not exist' meeting]
    n7 --> n8[Block Sep 31:<br/>Add 'Day does not exist' meeting]
    n8 --> n9[Block Nov 30:<br/>Add 'Day does not exist' meeting]
    n9 --> n10[Block Nov 31:<br/>Add 'Day does not exist' meeting]
    n10 --> stop([End])
```

**Paths**: 1 (sequential execution only)

**Defect**: Line 28 incorrectly blocks November 30, which is a valid date!

---

## 2. Calendar.check_times() CFG

```mermaid
graph TD
    start([Start: check_times<br/>m_month, m_day, m_start, m_end]) --> d1{m_day < 1 OR<br/>m_day > 30?}
    d1 -->|Yes| e1[Raise ConflictsException:<br/>'Day does not exist']
    d1 -->|No| d2{m_month < 1 OR<br/>m_month >= 12?}
    d2 -->|Yes| e2[Raise ConflictsException:<br/>'Month does not exist']
    d2 -->|No| d3{m_start < 0 OR<br/>m_start >= 23?}
    d3 -->|Yes| e3[Raise ConflictsException:<br/>'Illegal hour']
    d3 -->|No| d4{m_end < 0 OR<br/>m_end > 23?}
    d4 -->|Yes| e4[Raise ConflictsException:<br/>'Illegal hour']
    d4 -->|No| d5{m_start > m_end?}
    d5 -->|Yes| e5[Raise ConflictsException:<br/>'Meeting starts before it ends']
    d5 -->|No| n1[Return None]
    e1 --> stop1([Exception raised])
    e2 --> stop1
    e3 --> stop1
    e4 --> stop1
    e5 --> stop1
    n1 --> stop2([Normal return])
```

**Paths**: 6 (1 normal + 5 exception)

**Defects**:
- Line 63: `m_day > 30` should be month-specific or at least `> 31`
- Line 65: `m_month >= 12` should be `> 12` (December is month 12, valid!)
- Line 67: `m_start >= 23` should be `> 23` (hour  23 is 11 PM, valid!)

---

## 3. Calendar.is_busy() CFG

```mermaid
graph TD
    start([Start: is_busy<br/>month, day, start, end]) --> n1[busy = False]
    n1 --> n2[Call check_times<br/>month, day, start, end]
    n2 --> n3[Get meetings for<br/>occupied_month_day]
    n3 --> loop{For each<br/>meeting in<br/>that day}
    loop -->|More meetings| d1{start >= meeting.start_time<br/>AND<br/>start <= meeting.end_time?}
    d1 -->|Yes| n4[busy = True]
    d1 -->|No| d2{end >= meeting.start_time<br/>AND<br/>end <= meeting.end_time?}
    d2 -->|Yes| n5[busy = True]
    d2 -->|No| loop
    n4 --> loop
    n5 --> loop
    loop -->|No more meetings| n6[Return busy]
    n6 --> stop([End])
```

**Paths**: Multiple (depends on number of meetings and overlap conditions)

---

## 4. Calendar.add_meeting() CFG

```mermaid
graph TD
    start([Start: add_meeting<br/>to_add: Meeting]) --> n1[Extract month, day,<br/>start, end from to_add]
    n1 --> n2[Call check_times<br/>month, day, start, end]
    n2 --> d1{month not in<br/>occupied?}
    d1 -->|Yes| n3[Create new month dict]
    d1 -->|No| d2
    n3 --> d2{day not in<br/>occupied_month?}
    d2 -->|Yes| n4[Create new day list]
    d2 -->|No| n5
    n4 --> n5[Get that_day meetings list]
    n5 --> n6[booked = False<br/>conflict = None]
    n6 --> loop{For each<br/>meeting in<br/>that_day}
    loop -->|More meetings| d3{meeting.description !=<br/>'Day does not exist'?}
    d3 -->|Yes| d4{m_start >= meeting.start AND<br/>m_start <= meeting.end?}
    d3 -->|No| loop
    d4 -->|Yes| n7[booked = True<br/>conflict = meeting]
    d4 -->|No| d5{m_end >= meeting.start AND<br/>m_end <= meeting.end?}
    d5 -->|Yes| n8[booked = True<br/>conflict = meeting]
    d5 -->|No| loop
    n7 --> loop
    n8 --> loop
    loop -->|No more meetings| d6{booked?}
    d6 -->|Yes| e1[Raise ConflictsException<br/>with conflict details]
    d6 -->|No| n9[Append to_add to<br/>occupied_month_day]
    e1 --> stop1([Exception raised])
    n9 --> stop2([Normal return])
```

**Paths**: Many (branch combinations + loop iterations)

---

## 5. Calendar.print_agenda(month) CFG

```mermaid
graph TD
    start([Start: print_agenda<br/>month: int]) --> d1{month not in occupied<br/>OR<br/>no meetings in month?}
    d1 -->|Yes| n1[Return 'No Meetings<br/>booked for this month']
    d1 -->|No| n2[agenda = 'Agenda for month:']
    n2 --> loop1{For each day<br/>in month}
    loop1 -->|More days| loop2{For each meeting<br/>in day}
    loop2 -->|More meetings| n3[Append meeting<br/>to agenda string]
    n3 --> loop2
    loop2 -->|No more meetings| loop1
    loop1 -->|No more days| n4[Return agenda]
    n1 --> stop([End])
    n4 --> stop
```

**Paths**: 2 main paths (empty vs. non-empty month)

---

## 6. Calendar.print_agenda(month, day) CFG

```mermaid
graph TD
    start([Start: print_agenda<br/>month: int, day: int]) --> d1{month not in occupied OR<br/>day not in occupied_month OR<br/>no meetings on day?}
    d1 -->|Yes| n1[Return 'No Meetings<br/>booked on this date']
    d1 -->|No| n2[agenda = 'Agenda for month/day:']
    n2 --> loop{For each meeting<br/>in day}
    loop -->|More meetings| n3[Append meeting<br/>to agenda string]
    n3 --> loop
    loop -->|No more meetings| n4[Return agenda]
    n1 --> stop([End])
    n4 --> stop
```

**Paths**: 2 main paths (empty vs. non-empty day)

---

## 7. Calendar.clear_schedule() CFG

```mermaid
graph TD
    start([Start: clear_schedule<br/>month: int, day: int]) --> n1[occupied_month_day = empty list]
    n1 --> stop([End])
```

**Paths**: 1 (sequential only)

---

## 8. Calendar.get_meeting() CFG

```mermaid
graph TD
    start([Start: get_meeting<br/>month, day, index]) --> n1[Return occupied_month_day_index]
    n1 --> stop([End])
```

**Paths**: 1 (may raise IndexError if index invalid)

---

## 9. Calendar.remove_meeting() CFG

```mermaid
graph TD
    start([Start: remove_meeting<br/>month, day, index]) --> n1[Delete occupied_month_day_index]
    n1 --> stop([End])
```

**Paths**: 1 (may raise IndexError if index invalid)

---

## Summary

**Total Paths Analyzed**: Calendar class has multiple paths due to decision points in:
- `check_times()`: 6 paths
- `is_busy()`: Variable (based on meetings)
- `add_meeting()`: Many paths (complex branching)
- `print_agenda()`: 2-3 paths each overload
- Simple methods: 1 path each

**Statement Coverage Goal**: 100% - requires executing all paths including exception paths.
