#!/usr/bin/env python3
"""Entry script modo e2e: puntúa compliance.json e2e e informa.

Uso:
    python3 modes/e2e/run.py --compliance compliance.json [--outdir output/] [--target URL]
    python3 modes/e2e/run.py --checks a.json [b.json ...] [--outdir output/]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                "core", "utils"))

from orchestrator import main as orch_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(orch_main(["--mode", "e2e", *sys.argv[1:]]))
