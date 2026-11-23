"""Offline regressions for the organization continuity documentation gate."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_prime_directive.py"

class PrimeDirectiveGateTests(unittest.TestCase):
    def test_valid_repository_policy_passes(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("documentation-only gate", result.stdout)

    def test_missing_policy_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            copy = root / "scripts" / "check_prime_directive.py"
            copy.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
            result = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BLOCKED", result.stderr)

if __name__ == "__main__":
    unittest.main()
