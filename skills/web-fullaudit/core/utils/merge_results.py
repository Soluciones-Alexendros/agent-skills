#!/usr/bin/env python3
"""Fusiona resultados compliance + e2e en una lista unificada para score.py.

Entradas: uno o varios JSON (objeto con 'checks' o array directo, formato
compliance con 'resultado' o formato e2e con 'status'). Regla: un FAIL/WARN
nunca es pisado por un PASS posterior del mismo id; se conserva la evidencia
más completa.

Uso:
    python3 merge_results.py a.json b.json [--json fusion.json]
"""
import argparse
import json
import logging
import sys

logger = logging.getLogger("fullaudit.merge")


def _load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        raise RuntimeError(f"no se pudo leer {path}: {type(e).__name__}: {e}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON inválido en {path}: {e}") from e
    if isinstance(data, dict):
        return data.get("target"), data.get("checks", [])
    if isinstance(data, list):
        return None, data
    raise RuntimeError(f"formato inválido en {path}: se esperaba objeto o array")


def _estado(item):
    return ((item.get("resultado") or item.get("status") or "PENDING")).upper().replace("N/A", "NA")


def merge(listas):
    """Fusiona listas de checks; devuelve (target, checks)."""
    target = None
    mapa = {}
    orden = []
    for t, checks in listas:
        target = target or t
        for item in checks:
            if not isinstance(item, dict):
                continue
            cid = item.get("id") or item.get("script_key")
            if not cid:
                continue
            est = _estado(item)
            prev = mapa.get(cid)
            if prev and prev["_est"] in ("FAIL", "WARN") and est == "PASS":
                continue
            if prev and est == prev["_est"] and len(str(prev.get("evidencia"))) >= len(
                    str(item.get("evidencia") or item.get("evidence") or "")):
                pass
            merged = dict(item)
            merged["_est"] = est
            if "evidencia" not in merged and "evidence" in merged:
                merged["evidencia"] = merged["evidence"]
            if cid not in mapa:
                orden.append(cid)
            mapa[cid] = merged
    checks = []
    for cid in orden:
        m = dict(mapa[cid])
        m.pop("_est", None)
        checks.append(m)
    return target, checks


def main(argv=None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(description="Fusiona resultados compliance+e2e")
    ap.add_argument("entradas", nargs="+", help="JSON de resultados a fusionar")
    ap.add_argument("--json", help="Guardar fusión en JSON")
    args = ap.parse_args(argv)
    if not args.entradas:
        ap.error("se requiere al menos una entrada")
    try:
        listas = [_load(p) for p in args.entradas]
    except RuntimeError as e:
        logger.error("%s", e)
        return 2
    target, checks = merge(listas)
    out = {"target": target, "checks": checks, "fuentes": args.entradas}
    txt = json.dumps(out, ensure_ascii=False, indent=2)
    if args.json:
        try:
            with open(args.json, "w", encoding="utf-8") as fh:
                fh.write(txt)
        except OSError as e:
            logger.error("no se pudo escribir %s: %s: %s", args.json, type(e).__name__, e)
            print(txt)
            return 2
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
