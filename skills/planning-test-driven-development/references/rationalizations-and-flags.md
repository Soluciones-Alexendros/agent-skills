# Rationalizations, Red Flags, and Verification

## Common Rationalizations

| Rationalization                                    | Reality                                                                         |
| -------------------------------------------------- | ------------------------------------------------------------------------------- |
| "I will write tests after the code works"          | You will not. Tests written after the fact test implementation, not behavior.   |
| "This is too simple to test"                       | Simple code gets complicated. The test documents expected behavior.             |
| "Tests slow me down"                               | Tests slow you down now. They speed you up on every later change.               |
| "I tested it manually"                             | Manual testing does not persist. Tomorrow's change can break it silently.       |
| "The code is self-explanatory"                     | Tests are the specification: what the code should do, not what it does.         |
| "It is just a prototype"                           | Prototypes become production code. Tests from day one prevent test debt.        |
| "Let me run the tests again just to be extra sure" | After a clean run, repeating the same command adds nothing unless code changed. |
| "All tests pass" but no tests actually ran         | You must actually run the test command and confirm tests executed.              |

## Red Flags

- Writing code without any corresponding tests.
- Reaching for a default test command without checking what this repository uses.
- Tests that pass on the first run (they may not test what you think).
- "All tests pass" but no tests were actually run.
- Bug fixes without reproduction tests.
- Tests that check framework behavior instead of application behavior.
- Test names that do not describe expected behavior.
- Skipping tests to make the suite pass.
- Running the same test command twice in a row without any intervening code change.

## Verification Checklist

After completing any implementation:

- Every new behavior has a corresponding test.
- The full suite passes, run with the repository's own test command.
- Bug fixes include a reproduction test that failed before the fix.
- Test names describe the behavior being verified.
- No tests were skipped or disabled.
- Coverage has not decreased (if tracked).

Run each test command after a change that could affect the result. After a
clean run, do not repeat the same command unless the code has changed
since — re-running on unchanged code adds no confidence.
