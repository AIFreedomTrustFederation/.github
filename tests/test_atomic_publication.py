"""Regression tests for atomic catalog evidence publication."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_catalog_verification.py"
SPEC = importlib.util.spec_from_file_location("catalog_atomic_publication", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AtomicPublicationTests(unittest.TestCase):
    def test_success_replaces_complete_record(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            output.write_text('{"previous": true}\n')
            record = {"schema": "aift.verification.v1", "overall_status": "passed"}
            MODULE.write_record_atomically(output, record)
            self.assertEqual(json.loads(output.read_text()), record)
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_replace_failure_preserves_previous_record(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            previous = '{"previous": true}\n'
            output.write_text(previous)
            with patch.object(MODULE.os, "replace", side_effect=OSError("injected rename failure")):
                with self.assertRaises(OSError):
                    MODULE.write_record_atomically(output, {"overall_status": "failed"})
            self.assertEqual(output.read_text(), previous)
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_fsync_failure_preserves_previous_record(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            previous = '{"previous": true}\n'
            output.write_text(previous)
            with patch.object(MODULE.os, "fsync", side_effect=OSError("injected sync failure")):
                with self.assertRaises(OSError):
                    MODULE.write_record_atomically(output, {"overall_status": "failed"})
            self.assertEqual(output.read_text(), previous)
            self.assertEqual(list(Path(directory).iterdir()), [output])

    def test_failed_first_publication_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            with patch.object(MODULE.os, "fsync", side_effect=OSError("injected sync failure")):
                with self.assertRaises(OSError):
                    MODULE.write_record_atomically(output, {"overall_status": "passed"})
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
