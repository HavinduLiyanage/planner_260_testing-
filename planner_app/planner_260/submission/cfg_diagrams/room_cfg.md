# Control Flow Graph (CFG) - Room Class

## Overview

The `Room` class primarily serves as a wrapper around a `Calendar` object, associating it with a Room ID. Most methods delegate directly to the `Calendar` instance.

## 1. Room.__init__() CFG

```mermaid
graph TD
    start([Start: __init__<br/>id: str]) --> n1[self.id = id]
    n1 --> n2[self.calendar = Calendar()]
    n2 --> stop([End])
```

**Paths**: 1

---

## 2. Room.add_meeting() CFG

```mermaid
graph TD
    start([Start: add_meeting<br/>meeting: Meeting]) --> n1[Try block start]
    n1 --> n2[Call self.calendar.add_meeting(meeting)]
    n2 --> stop([End])
    n2 -.->|ConflictsException| e1[Catch ConflictsException]
    e1 --> e2[Raise new ConflictsException<br/>with room ID info]
    e2 --> stop1([Exception raised])
```

**Paths**: 2 (Normal, Exception)

---

## 3. Room.is_busy() CFG

```mermaid
graph TD
    start([Start: is_busy<br/>month, day, start, end]) --> n1[Return self.calendar.is_busy<br/>(month, day, start, end)]
    n1 --> stop([End])
```

**Paths**: 1 (Delegates logic to Calendar)

---

## 4. Room.print_agenda(month) CFG

```mermaid
graph TD
    start([Start: print_agenda<br/>month: int]) --> n1[Return self.calendar.print_agenda(month)]
    n1 --> stop([End])
```

**Paths**: 1

---

## 5. Room.print_agenda(month, day) CFG

```mermaid
graph TD
    start([Start: print_agenda<br/>month: int, day: int]) --> n1[Return self.calendar.print_agenda(month, day)]
    n1 --> stop([End])
```

**Paths**: 1

---

## 6. Room.get_meeting() CFG

```mermaid
graph TD
    start([Start: get_meeting<br/>month, day, index]) --> n1[Return self.calendar.get_meeting<br/>(month, day, index)]
    n1 --> stop([End])
```

**Paths**: 1

---

## 7. Room.remove_meeting() CFG

```mermaid
graph TD
    start([Start: remove_meeting<br/>month, day, index]) --> n1[Call self.calendar.remove_meeting<br/>(month, day, index)]
    n1 --> stop([End])
```

**Paths**: 1

---

## Summary

The `Room` class has low cyclomatic complexity as it delegates most operations. The main complexity lies in exception handling during `add_meeting`.
