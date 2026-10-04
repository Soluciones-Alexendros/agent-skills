# Using the skills

## Claude Code

Copy or link the skill folder into the user or project skills directory:

```bash
# global
cp -r skills/verify-owasp ~/.claude/skills/
# or per project
cp -r skills/verify-owasp /path/project/.claude/skills/
```

Claude Code discovers `SKILL.md` through its frontmatter (`name` + `description`).

## OpenAI Codex / compatible agents

Copy the folder to wherever the agent reads skills from (check its docs; `SKILL.md` + frontmatter is the open standard from [agentskills.io](https://agentskills.io)).

## Manual use

Each `SKILL.md` is self-contained and readable: its `references/` expand by levels and its `scripts/` automate the repeatable parts (see each skill's tools section).

## Choosing a skill

- By family: see the table in [README](../README.md) and [TAXONOMY.md](TAXONOMY.md).
- `description` fields declare explicit limits (`Not for X → other-skill`); on overlap, follow that pointer.

## Versioning

Each skill declares `metadata.version` in its frontmatter. When changing instructions, bump by magnitude:

```bash
python3 tools/version/bump.py --auto --type <major|minor|patch>
```

- `major`: incompatible update (breaking)
- `minor`: compatible new functionality
- `patch`: compatible fix

CI (`version.yml`) requires the bump on PRs with changed skills. To check locally:

```bash
python3 tools/version/bump.py --check --auto --base origin/main
```

The repo version lives in `package.json`. The annotated tag and GitHub Release are cut by `tools/version/cut_tag.py` from `main` when a changelog section has notes:

```bash
python3 tools/version/cut_tag.py --dry-run
```

## references/ structure (progressive loading)

Each skill follows the progressive loading pattern:

1. `SKILL.md` — self-contained start covering 80% of cases.
2. `references/` — detailed guides per topic, loaded only when the case needs them.
3. `scripts/` — automation utilities (never loaded into context, executed instead).

`build-upstash` adds `core/` and `modes/<mode>/` as internal router resources; they are not separate skills.

This keeps agent context light: only what the task needs gets read.

## Validation

Every skill must pass repo validation green:

```bash
bash run-validation.sh
```

Runs: spec (`skill_spec.py`), links (`skill_links.py`), release coherence, hygiene, version bump, pytest, smoke tests, and global `bash -n`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution process.
