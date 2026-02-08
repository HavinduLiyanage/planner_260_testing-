# Control Flow Graph (CFG) - Room Class

## Overview

The Room class acts as a wrapper around the Calendar class. Most methods delegate directly to the internal calendar object with added context (room ID) for error messages.

---

## 1. Room.__init__() CFG

```mermaid
graph TD
    start([Start: __init__<br/>id: str = ""]) --> n1[self.id = id]
    n1 --> n2[self.calendar = Calendar]
    n2 --> stop([End])
```

**Paths**: 1 (sequential only)

---

## 2. Room.get_id() CFG

```mermaid
graph TD
    start([Start: get_id]) --> n1[Return self.id]
    n1 --> stop([End])
```

**Paths**: 1 (sequential only)

---

## 3. Room.add_meeting() CFG

```mermaid
graph TD
    start([Start: add_meeting<br/>meeting: Meeting]) --> try[Try block]
    try --> n1[self.calendar.add_meeting<br/>meeting]
    n1 --> success[Success]
    success --> stop1([Normal return])
    try --> catch{Catch<br/>ConflictsException}
    catch --> n2[Raise ConflictsException with<br/>'Conflict for room id' message]
    n2 --> stop2([Exception raised])
```

**Paths**: 2 (success or exception)

**Key Feature**: Wraps calendar exception with room-specific context

---

## 4. Room.print_agenda() CFG

```mermaid
graph TD
    start([Start: print_agenda<br/>month: int, day: int = None]) --> d1{day is None?}
    d1 -->|Yes| n1[Return calendar.print_agenda<br/>month]
    d1 -->|No| n2[Return calendar.print_agenda<br/>month, day]
    n1 --> stop([End])
    n2 --> stop
```

**Paths**: 2 (month-only vs. month+day)

---

## 5. Room.is_busy() CFG

```mermaid
graph TD
    start([Start: is_busy<br/>month, day, start, end]) --> n1[Return calendar.is_busy<br/>month, day, start, end]
    n1 --> stop([End])
```

**Paths**: 1 (direct delegation)

---

## 6. Room.get_meeting() CFG

```mermaid
graph TD
    start([Start: get_meeting<br/>month, day, index]) --> n1[Return calendar.get_meeting<br/>month, day, index]
    n1 --> stop([End])
```

**Paths**: 1 (direct delegation)

---

## 7. Room.remove_meeting() CFG

```mermaid
graph TD
    start([Start: remove_meeting<br/>month, day, index]) --> n1[calendar.remove_meeting<br/>month, day, index]
    n1 --> stop([End])
```

**Paths**: 1 (direct delegation)

---

## Summary

**Architecture**: Delegation Pattern
- Room delegates to internal Calendar for all scheduling logic
- Adds room-specific context to exceptions
- Provides room identification via `get_id()`

**Total Paths**: 9 across all methods
- Most are simple delegations
- Only `add_meeting()` and `print_agenda()` have branches

**Statement Coverage**: Easy to achieve 100% as most methods are single-path delegations
