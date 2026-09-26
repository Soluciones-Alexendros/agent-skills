#!/usr/bin/env python3
"""Valida compliance.json contra checklist.schema.json (stdlib, sin jsonschema).

Verifica: array raíz, campos requeridos, enums (category/status/severity),
formato URI básico y tipos de evidence/rice.

Uso: python3 validate_compliance.py compliance.json
Salida: 0 válido · 1 inválido (errores en stdout) · 2 entrada ilegible o uso incorrecto.
"""
import argparse
import json
import logging
import os
import re
import sys

logger = logging.getLogger("e2e.validate")

HERE = os.path.dirname(os.path.abspath(__file__))
URI_RE = re.compile(r"^https?://[^\s]+$|^local://[^\s]+$")


def load_schema():
    path = os.path.join(HERE, "..", "assets", "schemas", "checklist.schema.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as e:
        raise RuntimeError(f"no se pudo leer schema {path}: {type(e).__name__}: {e}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"schema JSON inválido en {path}: {e}") from e


def validate(data, schema=None):
    schema = schema or load_schema()
    errors = []
    if not isinstance(data, list):
        return ["Raíz debe ser un array de checks"]
    props = schema["items"]["properties"]
    required = schema["items"]["required"]
    for i, item in enumerate(data):
        where = f"[{i}] id={item.get('id', '?')}" if isinstance(item, dict) else f"[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where}: entrada no es objeto")
            continue
        for req in required:
            if req not in item:
                errors.append(f"{where}: falta campo requerido '{req}'")
        for field in ("category", "status", "severity"):
            enum = props[field].get("enum")
            if field in item and item[field] not in enum:
                errors.append(f"{where}: {field}='{item[field]}' no está en {enum}")
        if "url" in item and not URI_RE.match(str(item["url"])):
            errors.append(f"{where}: url '{item['url']}' no es URI válida")
        ev = item.get("evidence")
        if ev is not None and not isinstance(ev, dict):
            errors.append(f"{where}: evidence debe ser objeto")
        rice = item.get("rice")
        if rice is not None:
            if not isinstance(rice, dict):
                errors.append(f"{where}: rice debe ser objeto")
            else:
                for k in ("reach", "impact", "confidence", "effort", "score"):
                    if k in rice and not isinstance(rice[k], (int, float)):
                        errors.append(f"{where}: rice.{k} debe ser numérico")
        # Regla de evidencia: FAIL exige evidencia mínima
        if item.get("status") == "FAIL":
            ev = item.get("evidence") or {}
            if not (ev.get("locator") or ev.get("screenshot") or ev.get("console")
                    or ev.get("network") or item.get("method")):
                errors.append(f"{where}: FAIL sin evidencia (locator/screenshot/console/method)")
    return errors


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Valida compliance.json contra checklist.schema.json")
    ap.add_argument("compliance", help="compliance.json a validar")
    args = ap.parse_args(argv)
    try:
        with open(args.compliance, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        logger.error("no se pudo leer %s: %s: %s", args.compliance, type(e).__name__, e)
        print(f"ERROR de lectura: {type(e).__name__}: {e}")
        return 2
    except json.JSONDecodeError as e:
        logger.error("JSON inválido en %s: %s", args.compliance, e)
        print(f"ERROR de lectura: JSONDecodeError: {e}")
        return 2
    except UnicodeDecodeError as e:
        logger.error("codificación inválida en %s: %s", args.compliance, e)
        print(f"ERROR de lectura: UnicodeDecodeError: {e}")
        return 2
    try:
        errors = validate(data)
    except RuntimeError as e:
        logger.error("%s", e)
        print(f"ERROR de schema: {e}")
        return 2
    if errors:
        print(f"INVÁLIDO — {len(errors)} error(es):")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"VÁLIDO — {len(data)} checks conformes al schema v2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
