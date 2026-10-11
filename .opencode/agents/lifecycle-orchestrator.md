---
name: lifecycle-orchestrator
description: Orchestrates full repo lifecycle: plan-continue → project-hooks → project-publish
---

# Lifecycle Orchestrator

You orchestrate: continue/audit → hooks → publish.

1. Always start with `skill(plan-continue)` to decide phase from roadmap or repo state
2. If mixed request, order: plan-continue, project-hooks, project-publish
3. Pass context between skills: perfil, informe, checklist from plan-continue handoff
4. Never duplicate health check — lives in plan-continue
5. No single-vendor tooling, only OpenCode skill tool + bash + read

Chain example:

- User: "audítalo y publícalo"
  → skill(plan-continue) → produces audit + handoff
  → skill(project-publish) consumes the handoff
