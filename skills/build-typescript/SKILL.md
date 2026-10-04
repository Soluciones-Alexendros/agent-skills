---
name: build-typescript
description: >-
  Advanced TypeScript typing: generics, conditional types, infer, branded types and typed API
  patterns. Use when there are complex types, difficult inference errors or typed API design.
  Do not use for security review (→ verify-owasp) nor general architecture (→ verify-architecture).
license: MIT
metadata:
  author: "Soluciones-Alexendros (adapted)"
  version: "2.0.0"
  domain: build
  type: atomic
  language: en
---

# Build TypeScript

## Overview

Advanced TypeScript typing: generics, conditional types, infer, branded types and typed API patterns.
Use when there are complex types, difficult inference errors or typed API design. Not for security review
nor general architecture.

## When to Use

- When there are complex types
- For difficult inference errors
- For typed API design

## Not for:

- Security review (→ verify-owasp)
- General architecture (→ verify-architecture)

## Advanced Types

### Generics

```typescript
function identity<T>(arg: T): T {
  return arg;
}
```

### Conditional Types

```typescript
type IsString<T> = T extends string ? "yes" : "no";
```

### Branded Types

```typescript
type UserId = string & { readonly brand: unique };
```
