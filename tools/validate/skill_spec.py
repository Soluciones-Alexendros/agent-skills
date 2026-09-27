#!/usr/bin/env python3
"""Validador de spec de skills (Agent Skills + STANDARD.md del repo).

Uso: python3 tools/validate/skill_spec.py [--root DIR]
Exit 0 si las 19 skills cumplen; 1 en caso contrario (lista errores).
Sin dependencias externas.
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PROHIBITED_DIRS = {"agents", "infrastructure", "languages"}
DOMINIOS = {"alignux", "codigo", "datos", "integraciones", "linux", "repo", "web"}
MAX_BODY_LINES = 500
ERRORS: list[str] = []


def err(skill: str, msg: str) -> None:
    ERRORS.append(f"[{skill}] {msg}")


def parse_frontmatter(text: str, skill: str) -> dict | None:
    if not text.startswith("---\n"):
        err(skill, "SKILL.md no empieza con '---'")
        return None
    end = text.find("\n---", 4)
    if end == -1:
        err(skill, "frontmatter sin cierre '---'")
        return None
    fm: dict[str, str] = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([a-z_]+):(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def check_skill(sdir: Path) -> None:
    skill = sdir.name
    f = sdir / "SKILL.md"
    if not f.is_file():
        err(skill, "falta SKILL.md")
        return
    text = f.read_text(encoding="utf-8")
    fm = parse_frontmatter(text, skill)
    if fm is None:
        return
    name = fm.get("name", "")
    if name != skill:
        err(skill, f"name '{name}' != carpeta '{skill}'")
    if not NAME_RE.match(name) or len(name) > 64:
        err(skill, f"name inválido: '{name}'")
    desc = fm.get("description", "")
    if not (1 <= len(desc) <= 1024):
        err(skill, f"description len={len(desc)} (1-1024)")
    if fm.get("license") != "MIT":
        err(skill, "license != MIT")
    body = text.split("\n---", 1)[-1]
    if len(body.splitlines()) > MAX_BODY_LINES:
        err(skill, f"cuerpo {len(body.splitlines())} líneas (> {MAX_BODY_LINES})")
    raw_fm = text[4:text.find("\n---", 4)]
    for key in ("author: Soluciones-Alexendros", "version:", "dominio:", "idioma: es"):
        if key not in raw_fm:
            err(skill, f"metadata sin '{key}'")
    dom = re.search(r"dominio:\s*(\S+)", raw_fm)
    if dom and dom.group(1) not in DOMINIOS:
        err(skill, f"dominio desconocido: {dom.group(1)}")
    ver = re.search(r"version:\s*\"?([^\"\s]+)\"?", raw_fm)
    if ver and not SEMVER_RE.match(ver.group(1)):
        err(skill, f"version no semver X.Y.Z: '{ver.group(1)}'")
    # directorios prohibidos dentro de la skill
    for d in PROHIBITED_DIRS:
        if (sdir / d).is_dir():
            err(skill, f"directorio prohibido: {d}/")
    # references/ solo ficheros planos
    refs = sdir / "references"
    if refs.is_dir():
        for sub in refs.iterdir():
            if sub.is_dir():
                err(skill, f"references/ contiene subdirectorio: {sub.name}/")
    # residuos prohibidos
    for pat in ("__pycache__", ".pytest_cache", "LICENSE", "LICENSE.txt"):
        if (sdir / pat).exists() or any(sdir.rglob(pat)):
            if pat in ("LICENSE", "LICENSE.txt") and (sdir / pat).is_file():
                err(skill, f"fichero {pat} por skill (licencia global)")
    if list(sdir.glob(".archivado*")):
        err(skill, "contiene .archivado*")


def main() -> int:
    if not SKILLS.is_dir():
        print(f"no existe {SKILLS}")
        return 1
    sdirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for s in sdirs:
        check_skill(s)
    print(f"skills: {len(sdirs)}, errores: {len(ERRORS)}")
    for e in ERRORS:
        print("FAIL", e)
    print("SPEC:", "OK" if not ERRORS else "CON-FALLOS")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
