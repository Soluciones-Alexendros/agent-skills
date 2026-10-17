---
name: lifecycle-orchestrator
description: Orchestrates full repo lifecycle: plan-continue → role-* → plan-validators → project-publish
---

# Lifecycle Orchestrator

You orchestrate: continue/audit → recurrent implementation roles → integrated validation → publish.

1. Always start with `skill(plan-continue)` to decide phase from roadmap or repo state
2. If mixed request, order: plan-continue, role-*, plan-validators, project-publish
3. Before every independent implementation action, re-evaluate and invoke all matching role-* skills; never treat the phase fallback as a one-time role assignment
4. Pass context and contracts between skills: perfil, informe, checklist and role handoffs
5. Never duplicate health check — lives in plan-continue
6. No single-vendor tooling, only OpenCode skill tool + bash + read

Chain example:

- User: "audítalo y publícalo"
  → skill(plan-continue) → produces audit + handoff
  → skill(project-publish) consumes the handoff
