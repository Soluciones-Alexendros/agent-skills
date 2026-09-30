#!/usr/bin/env python3
"""Validador de spec de skills (Agent Skills + STANDARD.md del repo).

Uso: python3 tools/validate/skill_spec.py [--root DIR]
Exit 0 si las 17 skills cumplen; 1 en caso contrario (lista errores).
Sin dependencias externas (usa yaml stdlib).
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML no instalado. pip install pyyaml")
    sys.exit(1)

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PROHIBITED_DIRS = {"agents", "infrastructure", "languages"}
DOMINIOS = {"disenar", "construir", "verificar", "operar"}
TIPOS = {"atomic", "router", "tecnologia"}
MAX_BODY_LINES = 500
MAX_BODY_TOKENS = 5000
ERRORS: list[str] = []

# Estimación simple de tokens: ~4 chars por token para español/inglés técnico
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


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
    fm_text = text[4:end]
    try:
        fm = yaml.safe_load(fm_text)
        if not isinstance(fm, dict):
            err(skill, "frontmatter no es un dict YAML válido")
            return None
    except yaml.YAMLError as e:
        err(skill, f"frontmatter YAML inválido: {e}")
        return None
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

    # name
    name = fm.get("name", "")
    if name != skill:
        err(skill, f"name '{name}' != carpeta '{skill}'")
    if not NAME_RE.match(name) or len(name) > 64:
        err(skill, f"name inválido: '{name}'")

    # description
    desc = fm.get("description", "")
    if not (1 <= len(desc) <= 1024):
        err(skill, f"description len={len(desc)} (1-1024)")

    # license
    if fm.get("license") != "MIT":
        err(skill, "license != MIT")

    # metadata
    meta = fm.get("metadata", {})
    if not isinstance(meta, dict):
        err(skill, "metadata debe ser un dict")
        return

    required_meta = {
        "author": "Soluciones-Alexendros",
        "version": None,  # any semver
        "dominio": None,  # any from DOMINIOS
        "tipo": None,     # any from TIPOS
        "idioma": "es",
    }
    for key, expected in required_meta.items():
        if key not in meta:
            err(skill, f"metadata sin '{key}'")
        elif expected is not None and meta[key] != expected:
            err(skill, f"metadata.{key}='{meta[key]}' esperado '{expected}'")

    # version semver
    ver = meta.get("version", "")
    if ver and not SEMVER_RE.match(str(ver)):
        err(skill, f"version no semver X.Y.Z: '{ver}'")

    # dominio closed set
    dom = meta.get("dominio", "")
    if dom and dom not in DOMINIOS:
        err(skill, f"dominio desconocido: {dom}")

    # tipo closed set
    tipo = meta.get("tipo", "")
    if tipo and tipo not in TIPOS:
        err(skill, f"tipo desconocido: {tipo} (debe ser uno de: {', '.join(sorted(TIPOS))})")

    # body lines + tokens
    body = text.split("\n---", 1)[-1]
    body_lines = len(body.splitlines())
    if body_lines > MAX_BODY_LINES:
        err(skill, f"cuerpo {body_lines} líneas (> {MAX_BODY_LINES})")
    body_tokens = estimate_tokens(body)
    if body_tokens > MAX_BODY_TOKENS:
        err(skill, f"cuerpo ~{body_tokens} tokens (> {MAX_BODY_TOKENS})")

    # prohibited dirs inside skill
    for d in PROHIBITED_DIRS:
        if (sdir / d).is_dir():
            err(skill, f"directorio prohibido: {d}/")

    # references/ only flat files
    refs = sdir / "references"
    if refs.is_dir():
        for sub in refs.iterdir():
            if sub.is_dir():
                err(skill, f"references/ contiene subdirectorio: {sub.name}/")

    # prohibited residues
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
