"""Black-box regression for GitHub Actions identity in catalog evidence."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_catalog_verification.py"

class CIIdentityTests(unittest.TestCase):
    def test_requires_complete_ci_identity_and_preserves_local_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            (root / "scripts").mkdir(parents=True)
            (root / "tests").mkdir()
            shutil.copy2(SCRIPT, root / "scripts" / SCRIPT.name)
            (root / "scripts" / "validate_repository_catalog.py").write_text("print('ok')\n")
            (root / "tests" / "test_ok.py").write_text(
                "import unittest\nclass T(unittest.TestCase):\n"
                "    def test_ok(self): self.assertTrue(True)\n")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test",
                            "-c", "user.email=test@example.invalid",
                            "commit", "-qm", "fixture"], check=True)
            sha = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            base = {**os.environ, "GITHUB_ACTIONS": "true", "GITHUB_SHA": sha,
                    "GITHUB_REPOSITORY": "AIFreedomTrustFederation/.github",
                    "GITHUB_RUN_ID": "12345"}
            cmd = [sys.executable, "-B", str(root / "scripts" / SCRIPT.name)]
            invalid = {
                "missing_sha": ("GITHUB_SHA", None),
                "wrong_sha": ("GITHUB_SHA", "b" * 40),
                "missing_repo": ("GITHUB_REPOSITORY", None),
                "wrong_repo": ("GITHUB_REPOSITORY", "other/repo"),
                "missing_run": ("GITHUB_RUN_ID", None),
                "zero_run": ("GITHUB_RUN_ID", "0"),
                "leading_zero": ("GITHUB_RUN_ID", "0123"),
                "nonnumeric_run": ("GITHUB_RUN_ID", "abc"),
                "oversized_run": ("GITHUB_RUN_ID", "9" * 5000),
            }
            for name, (key, value) in invalid.items():
                with self.subTest(name=name):
                    env = base.copy()
                    if value is None:
                        env.pop(key, None)
                    else:
                        env[key] = value
                    output = Path(tmp) / f"{name}.json"
                    result = subprocess.run(
                        [*cmd, "--output", str(output)], cwd=root, env=env,
                        capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertFalse(output.exists())
            output = Path(tmp) / "valid.json"
            result = subprocess.run(
                [*cmd, "--output", str(output)], cwd=root, env=base,
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            record = json.loads(output.read_text())
            self.assertEqual(record["overall_status"], "passed")
            self.assertEqual(record["source"]["run_url"],
                             "https://github.com/AIFreedomTrustFederation/.github/actions/runs/12345")
            local = base.copy()
            local["GITHUB_ACTIONS"] = "false"
            for key in ("GITHUB_SHA", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"):
                local.pop(key, None)
            output = Path(tmp) / "local.json"
            result = subprocess.run(
                [*cmd, "--output", str(output)], cwd=root, env=local,
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(output.read_text())["source"],
                             {"type": "local", "run_url": None})

if __name__ == "__main__":
    unittest.main()
