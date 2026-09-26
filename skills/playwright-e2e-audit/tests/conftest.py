"""Fixtures compartidos: scripts en sys.path (sin importar selftest)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
