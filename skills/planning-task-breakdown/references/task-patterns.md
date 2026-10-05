# Task Patterns

Dependency graphs, vertical slicing, and sizing rules extracted from the
planning-task-breakdown skill. Read this when ordering work or judging task size.

## Dependency Graph

Map what depends on what, then implement bottom-up (foundations first):

```text
Database schema
    │
    ├── API models/types
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI components
    │       │
    │       └── Validation logic
    │
    └── Seed data / migrations
```

## Horizontal vs Vertical Slicing

Build one complete feature path at a time instead of one full layer at a time.

Bad (horizontal slicing):

```text
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Connect everything
```

Good (vertical slicing):

```text
Task 1: User can create an account (schema + API + UI for registration)
Task 2: User can log in (auth schema + API + UI for login)
Task 3: User can create a task (task schema + API + UI for creation)
Task 4: User can view task list (query + API + UI for list view)
```

Each vertical slice delivers working, testable functionality.

## Sizing Guidelines

| Size   | Files | Scope                                 | Example                              |
| ------ | ----- | ------------------------------------- | ------------------------------------ |
| **XS** | 1     | Single function or config change      | Add a validation rule                |
| **S**  | 1-2   | One component or endpoint             | Add a new API endpoint               |
| **M**  | 3-5   | One feature slice                     | User registration flow               |
| **L**  | 5-8   | Multi-component feature               | Search with filtering and pagination |
| **XL** | 8+    | **Too large — break it down further** | —                                    |

An agent performs best on S and M tasks. If a task is L or larger, split it.

## When to Split a Task

- It would take more than one focused session (roughly 2+ hours of agent work).
- You cannot describe the acceptance criteria in 3 or fewer bullet points.
- It touches two or more independent subsystems (e.g., auth and billing).
- You find yourself writing "and" in the task title (a sign it is two tasks).
