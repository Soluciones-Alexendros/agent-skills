"""Tests de tools/validate/skill_spec.py."""
import importlib.util
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "skill_spec.py"


def load():
    spec = importlib.util.spec_from_file_location("skill_spec", SPEC)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_skill(root: Path, name: str, body: str, desc: str | None = None) -> None:
    skill = root / "skills" / name
    skill.mkdir(parents=True)
    description = desc or (
        f"Capacidad de {name}. Usar cuando el operador lo pida. "
        "No usar para otra familia."
    )
    (skill / "SKILL.md").write_text(
        f"""---
name: {name}
description: >-
  {description}
license: MIT
metadata:
  author: Soluciones-Alexendros
  version: "1.0.0"
  dominio: {name.split("-", 1)[0]}
  tipo: atomic
  idioma: es
---

# {name}

{body}
""",
        encoding="utf-8",
    )


def seed_catalog(root: Path, names: list[str]) -> None:
    rows = "\n".join(f"| `disenar` | {n} | x |" for n in names)
    (root / "README.md").write_text(
        f"| Familia | Skill | Qué hace |\n| --- | --- | --- |\n{rows}\n",
        encoding="utf-8",
    )
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "TAXONOMY.md").write_text(
        " · ".join(names) + "\n",
        encoding="utf-8",
    )


def run_root(root: Path) -> list[str]:
    mod = load()
    mod.ERRORS.clear()
    mod.ROOT = root
    mod.SKILLS = root / "skills"
    sdirs = mod.skill_dirs(root)
    names = {p.name for p in sdirs}
    mod.check_catalog(root, names)
    for s in sdirs:
        mod.check_skill(root, s, names)
    return list(mod.ERRORS)


def test_description_without_boundary(tmp_path):
    write_skill(
        tmp_path,
        "disenar-demo",
        "## Propósito\n\nX.\n\n## Cuándo usar\n\nY.\n\n## Referencias\n\nZ.\n",
        desc="Hace algo. Usar cuando pidas diseño.",
    )
    seed_catalog(tmp_path, ["disenar-demo"])
    errors = run_root(tmp_path)
    assert any("No usar para" in e for e in errors)


def test_arrow_to_missing_skill(tmp_path):
    write_skill(
        tmp_path,
        "disenar-demo",
        "## Propósito\n\nX.\n\n## Cuándo usar\n\nY.\n\n## Referencias\n\nZ.\n",
        desc="Hace algo. Usar cuando pidas diseño. No usar para seguridad (→ verificar-owasp).",
    )
    seed_catalog(tmp_path, ["disenar-demo"])
    errors = run_root(tmp_path)
    assert any("inexistente" in e for e in errors)


def test_host_profile_heading(tmp_path):
    write_skill(
        tmp_path,
        "operar-demo",
        "## Propósito\n\nX.\n\n## Cuándo usar\n\nY.\n\n"
        "## Perfil de Este Equipo\n\nhost.\n\n## Referencias\n\nZ.\n",
    )
    seed_catalog(tmp_path, ["operar-demo"])
    errors = run_root(tmp_path)
    assert any("H2 prohibido" in e for e in errors)


def test_catalog_mismatch(tmp_path):
    write_skill(
        tmp_path,
        "disenar-demo",
        "## Propósito\n\nX.\n\n## Cuándo usar\n\nY.\n\n## Referencias\n\nZ.\n",
    )
    seed_catalog(tmp_path, ["disenar-demo", "verificar-ghost"])
    errors = run_root(tmp_path)
    assert any("README vs carpetas" in e or "TAXONOMY vs carpetas" in e for e in errors)


def test_smoke_required_when_scripts(tmp_path):
    write_skill(
        tmp_path,
        "operar-demo",
        "## Propósito\n\nX.\n\n## Cuándo usar\n\nY.\n\n## Herramientas\n\ncli.\n\n## Referencias\n\nZ.\n",
    )
    scripts = tmp_path / "skills" / "operar-demo" / "scripts"
    scripts.mkdir()
    (scripts / "run.py").write_text("print(1)\n", encoding="utf-8")
    seed_catalog(tmp_path, ["operar-demo"])
    errors = run_root(tmp_path)
    assert any("smoke_sh.sh" in e for e in errors)
