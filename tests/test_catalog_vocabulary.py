"""Reject false-green catalog authority descriptions without changing policy values."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "scripts" / "validate_repository_catalog.py"
AUTHORITIES = (
    "canonical", "supporting", "incubating", "conceptual",
    "overlapping", "upstream-derived",
)


def fixture():
    return {
        "schema": "aift.repository-catalog.v1",
        "authority": "AIFreedomTrustFederation/.github",
        "authority_vocabulary": {key: f"meaning of {key}" for key in AUTHORITIES},
        "repositories": [{
            "name": "AIFT-OS", "layer": "control", "role": "control plane",
            "runtime": "Python", "authority": "canonical",
            "evidence": ["https://github.com/AIFreedomTrustFederation/AIFT-OS"],
        }],
        "census": {"organization": "AIFreedomTrustFederation"},
    }


class CatalogVocabularyTests(unittest.TestCase):
    def validate(self, payload):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "scripts" / VALIDATOR.name).write_bytes(VALIDATOR.read_bytes())
            (root / "federation.repositories.json").write_text(json.dumps(payload))
            return subprocess.run(
                [sys.executable, str(root / "scripts" / VALIDATOR.name)],
                text=True, capture_output=True, check=False,
            )

    def test_valid_descriptions_pass(self):
        result = self.validate(fixture())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_non_text_descriptions_rejected(self):
        for bad in (None, 0, False, [], {}):
            with self.subTest(bad=bad):
                payload = fixture()
                payload["authority_vocabulary"]["canonical"] = bad
                result = self.validate(payload)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("authority_vocabulary: canonical", result.stderr)

    def test_blank_descriptions_rejected(self):
        for bad in ("", " \t\n "):
            with self.subTest(bad=bad):
                payload = fixture()
                payload["authority_vocabulary"]["supporting"] = bad
                result = self.validate(payload)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("authority_vocabulary: supporting", result.stderr)


if __name__ == "__main__":
    unittest.main()
