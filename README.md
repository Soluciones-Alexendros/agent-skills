# agent-skills

25 engineering skills for coding agents, maintained by Soluciones-Alexendros under the MIT license. Skill names, domains, and content are in English; chats and outputs stay in Spanish.

## Quick start

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cp -r agent-skills/skills/<skill-name> ~/.agents/skills/
```

## OpenCode setup (primary harness)

OpenCode is the primary harness: no plugin system needed, only `AGENTS.md` + `opencode.json` (`skillDirectories`). The agent evaluates each request and maps it to a skill by description + keywords.

```bash
git clone https://github.com/Soluciones-Alexendros/agent-skills.git
cd agent-skills
bash scripts/install.sh            # global: ~/.config/opencode/skills, ~/.agents/skills, ~/.codex/skills, ~/.cursor/skills
bash scripts/install-opencode.sh   # project-local: .opencode/skills + .agents/skills
```

Verify routing with:

```bash
python tools/skill-router/route.py "limpia mi sistema Arch" --top 3
```

See `docs/harness-integration.md` (multi-harness table), `docs/opencode-setup.md`, and `docs/routing.md`.

## Skills by domain

25 skills across 4 active domains (`build`, `operate`, `planning`, `verify`). The `design` domain is reserved for future architecture skills and is currently empty.

### planning (4) — Planning and task breakdown

| Skill                                | Description                                                                                                                                                                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `planning-source-driven-development` | Source-driven development: verify every implementation decision against the official framework docs before coding. Use when starting unfamiliar work. Not for routine edits in known code.                               |
| `planning-test-driven-development`   | Red-green-refactor TDD cycle: failing test first, make it pass, refactor. For bugs, reproduce with a test first. Use when fixing bugs or adding behavior. Not for exploratory spikes.                                    |
| `planning-spec-driven-development`   | Structured spec before code: goal, commands, structure, style, testing, and limits. Gated flow: Spec → Plan → Tasks → Implement. Use when scoping multi-step work. Not for trivial one-line fixes.                       |
| `planning-task-breakdown`            | Break work into small verifiable tasks with explicit acceptance criteria. Vertical slicing ordered by dependencies, checkpoints every 2-3 tasks. Use when planning an implementation. Not for executing the work itself. |

### build (6) — Building, automation, and ecosystems

| Skill                 | Description                                                                                                                                                                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `build-automation`    | CI/CD pipeline automation: build, test, deploy. OS matrix, dependency caching, artifacts, stages, and jobs. Use when setting up pipelines. Not for release publishing (see `operate-release`).                                           |
| `build-design-system` | Build design systems: DTCG tokens (Style Dictionary, Figma Tokens), Tailwind v4, reusable component library. Use when creating tokens or UI kits. Not for one-screen visual direction (see `build-interface`).                           |
| `build-interface`     | Intentional visual direction for UI: type system, palette, layout, motion, signature element. Output is a justified visual design plan. Use when designing or restyling interfaces. Not for token pipelines (see `build-design-system`). |
| `build-proton-suite`  | Proton Mail (Bridge IMAP/SMTP local, MCP Mail) and Proton Pass (pass-cli JSON, MCP Pass). Read, search, and classify mail; fetch secrets; send email. Use when working with Proton. Not for other mail providers.                        |
| `build-typescript`    | Advanced TypeScript typing: generics, conditional types, infer, branded types, typed API patterns. Use for complex type logic. Not for security review (see `verify-owasp`) or architecture mapping (see `verify-architecture`).         |
| `build-upstash`       | Upstash ecosystem router (7 modes): Redis (cache, sessions, KV), Vector (embeddings, RAG), Search (full-text), QStash (queues, cron, workflows), Ratelimit, Blob, Box. Use when wiring Upstash services. Not for relational databases.   |

### verify (9) — Code audit, quality, and security

| Skill                 | Description                                                                                                                                                                                                                                                                        |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `verify-architecture` | Code architecture verification: structure analysis, dependency mapping, drift detection, refactor opportunities. Use when reviewing architecture. Not for security review (see `verify-owasp`).                                                                                    |
| `verify-compliance`   | Web compliance audit: accessibility (WCAG 2.2 AA), legal (GDPR, consent, cookies), on-page and off-page SEO. PASS/FAIL matrix, weighted scoring, RICE remediation plan. Use when auditing compliance. Not for performance (see `verify-performance`).                              |
| `verify-dependencies` | Dependency audit (SCA/CVE): multi-language pipeline (npm, pip, cargo, go, maven, gradle, composer, gem) for vulnerabilities, malware, typosquatting, unused and outdated deps. Produces SBOM. Use when scanning supply chain. Not for first-party code flaws (see `verify-owasp`). |
| `verify-fullaudit`    | Holistic web audit router: dispatches to `verify-compliance`, `verify-performance`, `verify-repo`, or `build-interface`. Use when asked for a full review without a focus. Not for executing the audits itself.                                                                    |
| `verify-hooks`        | Local git hooks: Husky, lint-staged, Prettier, typecheck, tests on commit; e2e on push when present. Use when gating commits locally. Not for remote CI (see `operate-release`).                                                                                                   |
| `verify-owasp`        | Code security review (OWASP): injection, XSS, authn/authz, crypto, SSRF, secrets, misconfiguration. Use when hunting vulnerabilities in code. Not for host hardening (see `operate-security`).                                                                                     |
| `verify-performance`  | Web performance audit: Core Web Vitals, Lighthouse, TTFB/FCP, rendering modes, HTTP and CDN caching, load optimization. Use when diagnosing slowness. Not for compliance (see `verify-compliance`).                                                                                |
| `verify-repo`         | Full repo audit and canonical plan start (repo starting): sync clone, status and roadmap board, contrast with repo standard, fix forward. Use when opening a plan. Not for closing releases (see `operate-release`).                                                               |
| `verify-testing`      | Testing verification and QA: test strategy, test quality review, coverage analysis, testing metrics. Use when assessing a suite. Not for writing the tests themselves.                                                                                                             |

### operate (6) — Linux operation, maintenance, and security

| Skill                 | Description                                                                                                                                                                                                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `operate-lifecycle`   | Work lifecycle router: plan start, hook gating via `verify-hooks`, or release closing via `operate-release`. Use when routing between phases. Not for executing audits, hooks, or releases.                                                          |
| `operate-maintenance` | Systematized Linux maintenance: hygiene, updates, cleanup, optimization. Graduated modes, read-only by default, risk-gated execution, reversible snapshots. Use when cleaning or tuning a host. Not for defensive security (see `operate-security`). |
| `operate-monitoring`  | Monitoring and observability setup: metrics, tracing, logs, alerting. Use when wiring dashboards and alerts. Not for incident forensics (see `operate-security`).                                                                                    |
| `operate-release`     | GitHub repo closing: version publishing, CI/CD audit, post-plan close-out. Semantic versioning, changelog, Actions supply chain. Use when shipping. Not for plan start (see `verify-repo`).                                                          |
| `operate-health`      | Linux health diagnosis: health checks, quick and full audits, system fingerprint, 0–100 health score. Use when assessing a machine. Not for cleanup execution (see `operate-maintenance`) or hardening (see `operate-security`).                     |
| `operate-security`    | Defensive Linux host security: posture, lightweight log forensics, CVEs, sysctl and SSH hardening, AppArmor/SELinux, auditd, fail2ban. Use when auditing or hardening a host. Not for app code flaws (see `verify-owasp`).                           |

## Naming and frontmatter

- Flat layout: `skills/<skill-name>/SKILL.md`.
- The `name` field is identical to the directory name: `<domain>-<slug>` in kebab-case. The prefix is the domain (normative, not advisory).
- Frontmatter carries exactly 6 keys: `name`, `description` (scope plus limits), `license: MIT`, `compatibility: "opencode, codex, cursor, copilot"`, `allowed-tools`, and `metadata` with `author`, `version` (semver), `domain`, `type`, `keywords`, and `language: en`.
- Closed type set: `atomic` (single capability) · `orchestrator` (multi-step workflow) · `router` (dispatches to other skills) · `audit` (read-only assessment with a report).

## Adding a new skill

Create a top-level directory (flat layout, no nesting):

```bash
mkdir -p skills/<skill-name>
```

Ship `SKILL.md` with standard frontmatter:

```yaml
---
name: <skill-name>
description: >-
  What it does. Use when the operator asks for it. Not for other families.
license: MIT
compatibility: "opencode, codex, cursor, copilot"
allowed-tools: "Read, Grep, Glob, Bash, Write"
metadata:
  author: Soluciones-Alexendros
  version: 3.0.0
  domain: build
  type: atomic
  language: en
  keywords: <skill-name>
---
```

Body must include `## Overview` and `## When to Use`. Skills bundling executable scripts also include `## Tools` and `scripts/tests/smoke_sh.sh`.

## Cross-references

Arrows (`→ other-skill`) in descriptions must resolve to an existing skill in this catalog.

## Validation

```bash
bash run-validation.sh
```

Checks: frontmatter schema, description scope clauses, heading canon, catalog parity between folders, README and TAXONOMY, reference resolution, and smoke tests.
