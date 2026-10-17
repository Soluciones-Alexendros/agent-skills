# Test Pyramid, Sizes, and Decision Guide

## Pyramid

```text
        ╱╲
       ╱  ╲         E2E Tests (~5%)
      ╱    ╲        Full user flows, real browser
     ╱──────╲
    ╱        ╲      Integration Tests (~15%)
   ╱          ╲     Component interactions, API boundaries
  ╱────────────╲
 ╱              ╲   Unit Tests (~80%)
╱                ╲  Pure logic, isolated, milliseconds each
╱──────────────────╲
```

If you liked it, you should have put a test on it. Keep most coverage at the
unit level; reserve E2E tests for critical user flows.

## Test Sizes

| Size   | Constraints                                            | Speed        | Example                                                |
| ------ | ------------------------------------------------------ | ------------ | ------------------------------------------------------ |
| Small  | Single process, no I/O, no network, no database        | Milliseconds | Pure function tests, data transforms                   |
| Medium | Multi-process OK, localhost only, no external services | Seconds      | API tests with test DB, component tests                |
| Large  | Multi-machine OK, external services allowed            | Minutes      | E2E tests, performance benchmarks, staging integration |

Small tests should make up the vast majority of the suite.

## Decision Guide

```text
Is it pure logic with no side effects?
  -> Unit test (small)

Does it cross a boundary (API, database, file system)?
  -> Integration test (medium)

Is it a critical user flow that must work end-to-end?
  -> E2E test (large) — limit these to critical paths
```
