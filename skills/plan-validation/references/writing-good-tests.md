# Writing Good Tests

## Test State, Not Interactions

Assert on the outcome of an operation, not on which methods were called
internally.

```text
// Good: tests what the function does (state-based)
it('returns tasks sorted by creation date, newest first', async () => {
  const tasks = await listTasks({ sortBy: 'createdAt', sortOrder: 'desc' });
  expect(tasks[0].createdAt.getTime())
    .toBeGreaterThan(tasks[1].createdAt.getTime());
});

// Bad: tests how the function works internally (interaction-based)
it('calls db.query with ORDER BY created_at DESC', async () => {
  await listTasks({ sortBy: 'createdAt', sortOrder: 'desc' });
  expect(db.query).toHaveBeenCalledWith(
    expect.stringContaining('ORDER BY created_at DESC')
  );
});
```

## DAMP Over DRY in Tests

In production code, DRY is usually right. In tests, prefer DAMP
(Descriptive And Meaningful Phrases): each test self-contained and readable.

```text
// DAMP: each test is self-contained and readable
it('rejects tasks with empty titles', () => {
  const input = { title: '', assignee: 'user-1' };
  expect(() => createTask(input)).toThrow('Title is required');
});

it('trims whitespace from titles', () => {
  const input = { title: '  Buy groceries  ', assignee: 'user-1' };
  const task = createTask(input);
  expect(task.title).toBe('Buy groceries');
});
```

Duplication in tests is acceptable when it makes each test independently
understandable. Avoid shared setup that obscures what a test verifies.

## Prefer Real Implementations Over Mocks

Preference order (most to least preferred):

```text
1. Real implementation  -> Highest confidence
2. Fake                 -> In-memory version of a dependency
3. Stub                 -> Returns canned data, no behavior
4. Mock (interaction)   -> Verifies method calls — use sparingly
```

Use test doubles only when the real implementation is too slow,
non-deterministic, or has side effects you cannot control. Mock only at
boundaries.

## Arrange-Act-Assert Pattern

```text
it('marks overdue tasks when deadline has passed', () => {
  // Arrange: set up the test scenario
  const task = createTask({
    title: 'Test',
    deadline: new Date('2025-01-01'),
  });

  // Act: perform the action being tested
  const result = checkOverdue(task, new Date('2025-01-02'));

  // Assert: verify the outcome
  expect(result.isOverdue).toBe(true);
});
```

## One Assertion Per Concept

```text
// Good: each test verifies one behavior
it('rejects empty titles', () => { ... });
it('trims whitespace from titles', () => { ... });
it('enforces maximum title length', () => { ... });

// Bad: everything in one test
it('validates titles correctly', () => {
  expect(() => createTask({ title: '' })).toThrow();
  expect(createTask({ title: '  hello  ' }).title).toBe('hello');
  expect(() => createTask({ title: 'a'.repeat(256) })).toThrow();
});
```

## Name Tests Descriptively

```text
// Good: reads like a specification
describe('TaskService.completeTask', () => {
  it('sets status to completed and records timestamp', ...);
  it('throws NotFoundError for non-existent task', ...);
  it('is idempotent — completing an already-completed task is a no-op', ...);
  it('sends notification to task assignee', ...);
});

// Bad: vague names
describe('TaskService', () => {
  it('works', ...);
  it('handles errors', ...);
  it('test 3', ...);
});
```

## Test Anti-Patterns to Avoid

| Anti-Pattern                          | Problem                                               | Fix                                                  |
| ------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| Testing implementation details        | Tests break on refactor even if behavior is unchanged | Test inputs and outputs, not internal structure      |
| Flaky tests (timing, order-dependent) | Erode trust in the suite                              | Use deterministic assertions, isolate test state     |
| Testing framework code                | Wastes time testing third-party behavior              | Only test your own code                              |
| Snapshot abuse                        | Large snapshots nobody reviews, break on any change   | Use snapshots sparingly and review every change      |
| No test isolation                     | Tests pass alone but fail together                    | Each test sets up and tears down its own state       |
| Mocking everything                    | Tests pass but production breaks                      | Prefer real implementations; mock only at boundaries |
