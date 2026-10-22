"""Regression tests for GitHub repository identity validation."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "scripts" / "validate_repository_catalog.py"


def entry(name, authority="canonical"):
    record = {
        "name": name,
        "layer": "control",
        "role": "test fixture",
        "runtime": "Go",
        "authority": authority,
        "evidence": [f"https://github.com/AIFreedomTrustFederation/{name}"],
    }
    if authority == "upstream-derived":
        record["upstream"] = "example/upstream"
    return record


def catalog(names):
    return {
        "schema": "aift.repository-catalog.v1",
        "authority": "AIFreedomTrustFederation/.github",
        "authority_vocabulary": {k: k for k in (
            "canonical", "supporting", "incubating", "conceptual",
            "overlapping", "upstream-derived")},
        "repositories": [entry(name) for name in names],
        "census": {"organization": "AIFreedomTrustFederation"},
    }


class CatalogIdentityTests(unittest.TestCase):
    def validate(self, names):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            (root / "scripts" / "validate_repository_catalog.py").write_bytes(VALIDATOR.read_bytes())
            (root / "federation.repositories.json").write_text(json.dumps(catalog(names)))
            return subprocess.run(
                [sys.executable, str(root / "scripts" / "validate_repository_catalog.py")],
                capture_output=True, text=True, check=False,
            )

    def test_distinct_repositories_pass(self):
        self.assertEqual(self.validate(["AIFT-OS", "AIFT-Forge"]).returncode, 0)

    def test_single_repository_passes(self):
        self.assertEqual(self.validate(["AIFT-OS"]).returncode, 0)

    def test_exact_duplicate_rejected(self):
        result = self.validate(["AIFT-OS", "AIFT-OS"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate repository name", result.stderr)


    def test_invalid_repository_names_rejected(self):
        for name in ("../outside", "AIFT-OS?tab=readme", "AIFT-OS#readme", "AIFT/OS", "AIFT%2FOS", "AIFT OS", ".", "..", "x" * 101):
            with self.subTest(name=name):
                result = self.validate([name])
                self.assertNotEqual(result.returncode, 0, f"invalid repository name accepted: {name!r}")
                self.assertIn("invalid GitHub repository name", result.stderr)

    def test_valid_dotted_repository_names_pass(self):
        result = self.validate([".github", "www.aifreedomtrust.com", "c-848263", "aift_runtime"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_case_alias_rejected(self):
        result = self.validate(["AIFT-OS", "aift-os"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate repository name", result.stderr)


if __name__ == "__main__":
    unittest.main()
