# Citation Guide

How to cite sources for framework-specific decisions.

## In Code Comments

```text
// React 19 form handling with useActionState
// Source: https://react.dev/reference/react/useActionState#usage
const [state, formAction, isPending] = useActionState(submitOrder, initialState);
```

## In Conversation

```text
I'm using useActionState instead of manual useState for the form submission state.
React 19 replaced the manual isPending/setIsPending pattern with this hook.

Source: https://react.dev/blog/2024/12/05/react-19#actions
"useTransition now supports async functions [...] to handle pending states automatically"
```

## Rules

- Full URLs, not shortened; prefer deep links with anchors where possible.
- Quote the relevant passage when it supports a non-obvious decision.
- Include browser/runtime support data when recommending platform features.
- If you cannot find documentation for a pattern, say so explicitly:

```text
UNVERIFIED: I could not find official documentation for this pattern.
This is based on training data and may be outdated.
Verify before using in production.
```

Honesty about what you couldn't verify is more valuable than false confidence.

## Conflict Template

When docs conflict with existing project code, surface it instead of silently picking one:

```text
CONFLICT DETECTED:
The existing codebase uses useState for form loading state,
but React 19 docs recommend useActionState for this pattern.
(Source: react.dev/reference/react/useActionState)

Options:
A) Use the modern pattern (useActionState) — consistent with current docs
B) Match existing code (useState) — consistent with codebase
→ Which approach do you prefer?
```
