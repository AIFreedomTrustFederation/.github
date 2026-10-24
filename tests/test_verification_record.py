"""Truthfulness regressions for machine-readable catalog verification evidence."""

import importlib.util
import json
import os
import shutil
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_catalog_verification.py"
SPEC = importlib.util.spec_from_file_location("catalog_verification", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
SHA = "a" * 40


class VerificationRecordTests(unittest.TestCase):
    def test_all_passed_is_passed_and_limits_are_explicit(self):
        checks = MODULE.execute_checks(Path("/tmp"), runner=lambda *a, **k: subprocess.CompletedProcess(a, 0, "", ""))
        record = MODULE.build_record(SHA, checks, "local", None)
        self.assertEqual(record["overall_status"], "passed")
        self.assertEqual(record["commit_sha"], SHA)
        self.assertEqual(record["security"]["status"], "not_checked")
        self.assertEqual(record["dependencies"]["status"], "not_checked")
        self.assertEqual(record["deployment"]["status"], "not_applicable")
        self.assertEqual([c["id"] for c in checks], ["catalog", "regression"])

    def test_failed_check_is_not_reported_as_passed_and_next_check_runs(self):
        called = []
        def runner(command, **kwargs):
            called.append(command)
            return subprocess.CompletedProcess(command, 1 if len(called) == 1 else 0, "", "")
        checks = MODULE.execute_checks(Path("/tmp"), runner=runner)
        record = MODULE.build_record(SHA, checks, "github-actions", "https://github.com/example/run")
        self.assertEqual([c["status"] for c in checks], ["failed", "passed"])
        self.assertEqual(record["overall_status"], "failed")
        self.assertEqual(len(called), 2)

    def test_missing_executable_fails_closed(self):
        def runner(*a, **k):
            raise FileNotFoundError("python missing")
        checks = MODULE.execute_checks(Path("/tmp"), runner=runner)
        self.assertEqual([c["exit_code"] for c in checks], [127, 127])
        self.assertEqual(MODULE.build_record(SHA, checks, "local", None)["overall_status"], "failed")

    def test_rejects_invalid_commit_identity(self):
        for sha in ("", "a" * 39, "A" * 40, "g" * 40):
            with self.subTest(sha=sha):
                with self.assertRaises(ValueError):
                    MODULE.build_record(sha, [], "local", None)

    def test_empty_checks_never_pass(self):
        self.assertEqual(MODULE.build_record(SHA, [], "local", None)["overall_status"], "failed")

    def test_cli_records_real_exit_codes_and_checked_out_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            shutil.copy2(SCRIPT, root / "scripts" / SCRIPT.name)
            (root / "scripts" / "validate_repository_catalog.py").write_text(
                "import pathlib, sys\nsys.exit(1 if pathlib.Path('bad').exists() else 0)\n"
            )
            (root / "tests" / "test_example.py").write_text(
                "import unittest\nclass Example(unittest.TestCase):\n"
                "    def test_pass(self): self.assertTrue(True)\n"
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Test",
                            "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], check=True)
            sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            env = {**os.environ, "GITHUB_SHA": sha, "GITHUB_REPOSITORY": MODULE.REPOSITORY}
            output = root / "report.json"
            cmd = [sys.executable, "-B", str(root / "scripts" / SCRIPT.name), "--output", str(output)]
            success = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(success.returncode, 0, success.stderr)
            record = json.loads(output.read_text())
            self.assertEqual(record["commit_sha"], sha)
            self.assertEqual(record["overall_status"], "passed")
            (root / "bad").write_text("trigger failure")
            failure = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(failure.returncode, 1, failure.stderr)
            record = json.loads(output.read_text())
            self.assertEqual(record["overall_status"], "failed")
            self.assertEqual([c["status"] for c in record["checks"]], ["failed", "passed"])
            output.unlink()
            env["GITHUB_SHA"] = "b" * 40
            mismatch = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(mismatch.returncode, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
