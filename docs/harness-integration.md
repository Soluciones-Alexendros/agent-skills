# Harness integration status

Classification of agent harnesses for autoworkspace skills.

| Harness  | Status                                                                                                      | Evidence                                                |
| -------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| OpenCode | documented-not-proven (level B) until a real binary of a declared version passes discovery/permission tests | `opencode.json`, `scripts/install-opencode.sh --target` |
| Cursor   | documented-not-proven                                                                                       | project `skills/` + optional `.agents/skills` symlinks  |
| Codex    | documented-not-proven                                                                                       | install target via `scripts/install.sh --target`        |
| Copilot  | documented-not-proven                                                                                       | folder layout only                                      |

## OpenCode acceptance levels

- **A (required for contracts):** configuration and adapter tests with doubles (`tools/execution`, `tools/contracts`).
- **B (required to claim verified OpenCode support):** real binary of a declared version loads a skill by name and denies action permissions independently of load permissions. Auto-approval modes must not be used in those tests.

If the binary is unavailable, level B is `not_run` and support must not be advertised as verified.

## Permissions

Loading a skill does not authorize Bash, network, secrets, or paths outside the project. Product restrictions remain even when the harness can load the skill file.
