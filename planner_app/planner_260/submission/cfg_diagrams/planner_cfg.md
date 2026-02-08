# Control Flow Graph (CFG) - Planner Class

## Overview

The `Planner` class handles the user interface and main application logic. It interacts with the `Organization` class to manage scheduling.

## 1. Planner.main_menu() CFG

```mermaid
graph TD
    start([Start: main_menu]) --> n1[Print Welcome]
    n1 --> n2[user_input = 999]
    n2 --> loop{user_input != 0?}
    loop -->|No| stop([End])
    loop -->|Yes| n3[Print Menu Options]
    n3 --> n4[Try block start]
    n4 --> n5[Get user_input]
    n5 --> d1{user_input == 1?}
    d1 -->|Yes| c1[Call sched_vac()]
    d1 -->|No| d2{user_input == 2?}
    d2 -->|Yes| c2[Call sched_meet()]
    d2 -->|No| d3{user_input == 3?}
    d3 -->|Yes| c3[Call check_room_availability()]
    d3 -->|No| d4{user_input == 4?}
    d4 -->|Yes| c4[Call check_employee_availability()]
    d4 -->|No| d5{user_input == 5?}
    d5 -->|Yes| c5[Call check_agenda_room()]
    d5 -->|No| d6{user_input == 6?}
    d6 -->|Yes| c6[Call check_agenda_person()]
    d6 -->|No| d7{user_input == 0?}
    d7 -->|Yes| c7[exit()]
    d7 -->|No| c8[Print 'Enter 0-6']
    c1 --> loop
    c2 --> loop
    c3 --> loop
    c4 --> loop
    c5 --> loop
    c6 --> loop
    c8 --> loop
    n5 -.->|ValueError| e1[Catch ValueError]
    e1 --> e2[Print 'Invalid number']
    e2 --> loop
    c7 --> stop
```

## 2. Planner.sched_meet() CFG

```mermaid
graph TD
    start([Start: sched_meet]) --> n1[successful = True]
    n1 --> n2[Get month, day, start, end]
    n2 --> n3[Print open rooms]
    n3 --> loop1{For each room<br/>in org.get_rooms()}
    loop1 -->|More| d1{room not busy?}
    d1 -->|Yes| n4[Print room ID]
    d1 -->|No| loop1
    n4 --> loop1
    d1 -.->|ConflictsException| e1[Print Error]
    e1 --> stop_err([Return])
    loop1 -->|Done| n5[selected_room = None]
    n5 --> loop2{not selected_room?}
    loop2 -->|No| n6[Print people available]
    loop2 -->|Yes| n7[Get room_id input]
    n7 --> d2{room_id == 'cancel'?}
    d2 -->|Yes| stop_cancel([Return])
    d2 -->|No| n8[Try get_room]
    n8 --> n9[selected_room = room]
    n9 --> loop2
    n8 -.->|Exception| e2[Print Error]
    e2 --> loop2
    n6 --> loop3{For each person<br/>in org.get_employees()}
    loop3 -->|More| d3{person not busy?}
    d3 -->|Yes| n10[Print person name]
    d3 -->|No| loop3
    n10 --> loop3
    d3 -.->|Exception| e3[Print Error]
    e3 --> stop_err
    loop3 -->|Done| n11[attendees = []]
    n11 --> loop4{True}
    loop4 --> n12[Get name input]
    n12 --> d4{name == 'done'?}
    d4 -->|Yes| n13[Get description]
    d4 -->|No| n14[Try get_employee]
    n14 --> n15[Append to attendees]
    n15 --> loop4
    n14 -.->|Exception| e4[Print Error]
    e4 --> loop4
    n13 --> n16[Create Meeting object]
    n16 --> n17[Try add meeting to room<br/>and attendees]
    n17 --> d5{successful?}
    d5 -->|Yes| n18[Print Success]
    d5 -->|No| n19[Print Error (handled in except)]
    n18 --> stop([End])
    n19 --> stop
    n17 -.->|ConflictsException| e5[successful=False<br/>Print Error]
    e5 --> d5
```

## 3. Planner.sched_vac() CFG

```mermaid
graph TD
    start([Start: sched_vac]) --> n1[successful = True]
    n1 --> n2[Get employee name]
    n2 --> n3[Try get_employee]
    n3 --> n4[Get start/end dates]
    n3 -.->|Exception| e1[Print Error]
    e1 --> stop_err([Return])
    n4 --> loop1{For month in range}
    loop1 -->|More| loop2{For day in range}
    loop2 -->|More| n5[Try add_meeting(Vacation)]
    n5 --> loop2
    n5 -.->|ConflictsException| e2[successful = False<br/>Print Error]
    e2 --> stop_err
    loop2 -->|Done| loop1
    loop1 -->|Done| d1{successful?}
    d1 -->|Yes| n6[Print Success]
    d1 -->|No| stop([End])
    n6 --> stop
```

## Summary

The `Planner` class contains the main control loops and user interaction logic. `main_menu` drives the application, while `sched_meet` and `sched_vac` handle complex multi-step input processes and coordination between `Room` and `Person` objects.
