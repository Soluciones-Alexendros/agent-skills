# Skill taxonomy

25 skills in 5 domains. The `metadata.domain` frontmatter field reflects this table, and the name prefix is the domain (normative, not advisory). The taxonomy is closed: every new skill must fit an existing domain or propose a new one in the PR (see CONTRIBUTING.md).

| Domain     | Scope                                                     | Skills                                                                                                                                                             |
| ---------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `build`    | Building: typing, automation, data, integrations          | build-automation · build-design-system · build-interface · build-proton-suite · build-typescript · build-upstash                                                   |
| `operate`  | Publishing and continuous operation                       | operate-lifecycle · operate-mantenimiento · operate-monitoring · operate-release · operate-salud-sistema · operate-seguridad                                       |
| `planning` | Work planning and decomposition                           | planning-source-driven-development · planning-spec-driven-development · planning-task-breakdown · planning-test-driven-development                                 |
| `verify`   | Quality gates and audits                                  | verify-architecture · verify-compliance · verify-dependencias · verify-fullaudit · verify-hooks · verify-owasp · verify-performance · verify-repo · verify-testing |
| `design`   | Reserved for future architecture skills (currently empty) | —                                                                                                                                                                  |

## Closed sets (normative)

**Domain** (metadata.domain): `build` | `design` | `operate` | `planning` | `verify`

**Type** (metadata.type): `atomic` | `orchestrator` | `router` | `audit`

- `atomic`: single-capability skill, executed directly
- `orchestrator`: runs a multi-step workflow end to end
- `router`: dispatches to other skills (runs no domain logic itself)
- `audit`: read-only assessment producing findings and a remediation plan

## Rules

1. The `name` frontmatter field in `SKILL.md` is identical to the directory name.
2. The `metadata.domain` field reflects this table — the name prefix IS the domain (normative, not advisory): every skill is named `<domain>-<slug>` in kebab-case.
3. The `metadata.type` field is required and must be one of the closed set; `metadata.language` is `en`.
4. The `description` field declares scope and limits (`Use when` plus an exclusion clause) with cross-references (`→ other-skill`) where scopes overlap; every arrow target must exist.
5. Body has `## Overview` and `## When to Use`; skills bundling executables also have `## Tools` plus `scripts/tests/smoke_sh.sh`.
