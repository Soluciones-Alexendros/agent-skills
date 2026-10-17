"""Tests for status_bump."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from status_bump import advance_status, load_status  # noqa: E402


class TestStatusBump(unittest.TestCase):
    def test_refuse_without_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".autoworkspace").mkdir()
            with self.assertRaises(ValueError):
                advance_status(root, phase="DEFINE", skill="plan-specification")

    def test_advance_state_revision_without_product_semver(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".autoworkspace").mkdir()
            s1 = advance_status(
                root, phase="DEFINE", skill="plan-specification", evidence_ok=True
            )
            self.assertEqual(s1["advance"], 1)
            self.assertEqual(s1["state_revision"], 1)
            self.assertEqual(s1["version"], "0.1.0")  # product SemVer unchanged
            s2 = advance_status(
                root,
                phase="INTEGRATE",
                skill="project-publish",
                evidence_ok=True,
                bump_product_version=True,
            )
            self.assertEqual(s2["version"], "0.2.0")
            loaded = load_status(root)
            self.assertEqual(loaded["advance"], 2)
            self.assertEqual(len(loaded["history"]), 2)


if __name__ == "__main__":
    unittest.main()
