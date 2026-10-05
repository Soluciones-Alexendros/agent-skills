# Spec Quality: Living Spec, Rationalizations, Red Flags, Verification

Companion to `planning-spec-driven-development`. Detail kept out of the SKILL.md body.

## Keeping the Spec Alive

The spec is a living document, not a one-time artifact:

- **Update when decisions change** — if the data model needs to change, update the spec first, then implement.
- **Update when scope changes** — features added or cut are reflected in the spec.
- **Commit the spec** — it belongs in version control alongside the code.
- **Reference the spec in PRs** — link back to the spec section each PR implements.

## Common Rationalizations

| Rationalization                       | Reality                                                                                                                                                                                |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "This is simple, I don't need a spec" | Simple tasks don't need _long_ specs, but they still need acceptance criteria. A two-line spec is fine.                                                                                |
| "I'll write the spec after I code it" | That's documentation, not specification. The spec's value is in forcing clarity _before_ code.                                                                                         |
| "The spec will slow us down"          | A 15-minute spec prevents hours of rework. Waterfall in 15 minutes beats debugging in 15 hours.                                                                                        |
| "Requirements will change anyway"     | That's why the spec is a living document. An outdated spec is still better than no spec.                                                                                               |
| "The user knows what they want"       | Even clear requests have implicit assumptions. The spec surfaces those assumptions.                                                                                                    |
| "I'll decompose during planning"      | Planning slices tasks within a spec. By then the oversized artifact already exists — module boundaries and dependency direction must be decided before the spec is written, not after. |

## Red Flags

- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
- Making architectural decisions without documenting them
- Skipping the spec because "it's obvious what to build"
- Writing the spec and starting the plan or code in the same turn
- One spec whose requirements span several independently testable capabilities
- Module boundaries or build order decided implicitly during implementation because no capability map was approved up front

## Verification Checklist

Before proceeding to implementation, confirm:

- The spec covers all six core areas
- The human has reviewed and approved the spec
- The turn ended after saving the spec; approval came in a later turn
- Success criteria are specific and testable
- Boundaries (Always/Ask First/Never) are defined
- The spec is saved to a file in the repository
- If the request bundles several independently testable capabilities, a capability map (module ids, dependency direction, build order) was approved before any module spec was written
- Every module spec traces to a module id in the approved map
