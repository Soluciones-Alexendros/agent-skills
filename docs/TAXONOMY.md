# Skill taxonomy

19 skills in 5 domains. The `metadata.domain` frontmatter field reflects this table, and the name prefix is the domain (normative, not advisory). The taxonomy is closed: every new skill must fit an existing domain or propose a new one in the PR (see CONTRIBUTING.md).

| Domain    | Scope                                                                                    | Skills                                                                                       |
| --------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `plan`    | How work is decided: specification, continuation, validation                             | plan-specification · plan-continue · plan-validation                                         |
| `system`  | Local OS and workstation tooling (not online DevOps)                                     | system-health · system-maintenance · system-security · system-proton                         |
| `project` | Static repository concerns: docs, config, versioning, packaging, local quality           | project-architecture · project-hooks · project-libraries · project-publish · project-testing |
| `web`     | Dynamic behavior of a deployed, internet-accessible project                              | web-compliance · web-owasp · web-performance                                                 |
| `role`    | Specialist implementation agents with executable methods (replace vague persona prompts) | role-back · role-clean-code · role-design · role-front                                       |

## Closed sets (normative)

**Domain** (metadata.domain): `plan` | `system` | `project` | `web` | `role`

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
