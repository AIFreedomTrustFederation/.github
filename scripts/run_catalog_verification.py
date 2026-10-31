#!/usr/bin/env python3
"""Execute catalog gates and emit a commit-bound, machine-readable evidence record."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "AIFreedomTrustFederation/.github"
CHECKS = (
    ("catalog", "python -B scripts/validate_repository_catalog.py",
     ("-B", "scripts/validate_repository_catalog.py")),
    ("regression", "python -B -m unittest discover -s tests -v",
     ("-B", "-m", "unittest", "discover", "-s", "tests", "-v")),
)


def execute_checks(root: Path, python: str = sys.executable, runner=subprocess.run) -> list[dict]:
    results = []
    for check_id, command, args in CHECKS:
        try:
            result = runner([python, *args], cwd=root, capture_output=True, text=True, check=False)
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            exit_code = result.returncode
        except OSError as error:
            print(f"{check_id}: could not execute: {error}", file=sys.stderr)
            exit_code = 127
        results.append({
            "id": check_id, "command": command,
            "status": "passed" if exit_code == 0 else "failed",
            "exit_code": exit_code,
        })
    return results



def check_worktree(root: Path) -> dict:
    """Fail commit-bound evidence if tracked or untracked checkout content differs."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=root, capture_output=True, text=True, check=False,
        )
        exit_code = result.returncode or (1 if result.stdout else 0)
    except OSError:
        exit_code = 127
    return {
        "id": "worktree", "command": "git status --porcelain --untracked-files=normal",
        "status": "passed" if exit_code == 0 else "failed",
        "exit_code": exit_code,
    }


def build_record(commit: str, checks: list[dict], source: str, run_url: str | None) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("commit must be an exact 40-character lowercase Git SHA")
    if source not in ("local", "github-actions"):
        raise ValueError("unknown verification source")
    return {
        "schema": "aift.verification.v1",
        "repository": REPOSITORY,
        "commit_sha": commit,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": {"type": source, "run_url": run_url},
        "checks": checks,
        "overall_status": "passed" if checks and all(c["status"] == "passed" for c in checks) else "failed",
        "security": {"status": "not_checked", "reason": "No security scan is performed by this gate."},
        "dependencies": {"status": "not_checked", "reason": "Cross-repository dependencies are not validated."},
        "deployment": {"status": "not_applicable", "reason": "No deployment is performed by this gate."},
        "limitations": [
            "This record covers only the local catalog validator and Python regression tests.",
            "It does not establish repository census completeness or live integration health.",
            "The JSON is an unsigned CI artifact, not a cryptographic attestation.",
            "Worktree checks do not detect ignored files or external runtime state.",
        ],
    }


def write_record_atomically(output: Path, record: dict) -> None:
    """Replace evidence only after a complete, flushed same-directory write."""
    output.parent.mkdir(parents=True, exist_ok=True)
    staged = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=output.parent,
            prefix=f".{output.name}.", suffix=".tmp", delete=False,
        ) as handle:
            staged = Path(handle.name)
            handle.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, output)
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        # Verification must never create or overwrite files inside the
        # checkout after its clean-worktree checks have completed.
        output = args.output.resolve()
        if output.is_relative_to(ROOT.resolve()):
            raise ValueError("verification output must be outside the repository checkout")
        sha_result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT,
            capture_output=True, text=True, check=True,
        )
        commit = sha_result.stdout.strip()
        source = "github-actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local"
        expected = os.environ.get("GITHUB_SHA")
        github_repo = os.environ.get("GITHUB_REPOSITORY")
        run_id = os.environ.get("GITHUB_RUN_ID")
        if source == "github-actions":
            # In CI, absent identity must never produce passing evidence.
            if expected != commit:
                raise ValueError("GITHUB_SHA must match the checked-out commit")
            if github_repo != REPOSITORY:
                raise ValueError("GITHUB_REPOSITORY must match the catalog owner")
            if not run_id or not re.fullmatch(r"[1-9][0-9]{0,19}", run_id):
                raise ValueError("GITHUB_RUN_ID must be a positive canonical decimal run ID")
        else:
            # Preserve existing local verification behavior.
            if expected and expected != commit:
                raise ValueError("GITHUB_SHA does not match the checked-out commit")
            if github_repo and github_repo != REPOSITORY:
                raise ValueError("GITHUB_REPOSITORY does not match the catalog owner")
        run_url = (f"https://github.com/{REPOSITORY}/actions/runs/{run_id}"
                   if source == "github-actions" else None)
        # Check both sides of execution: a dirty checkout or tests that mutate
        # the checkout must never yield a successful commit-bound record.
        before = check_worktree(ROOT)
        checks = execute_checks(ROOT)
        after = check_worktree(ROOT)
        # A clean worktree alone does not prove commit stability: a check
        # can create an empty commit and move HEAD without changing files.
        try:
            final_head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=ROOT,
                capture_output=True, text=True, check=False,
            )
            head_code = final_head.returncode or (0 if final_head.stdout.strip() == commit else 1)
        except OSError:
            head_code = 127
        worktree_code = before["exit_code"] or after["exit_code"] or head_code
        checks.append({
            "id": "worktree",
            "command": before["command"] + " (before and after); git rev-parse HEAD (after)",
            "status": "passed" if worktree_code == 0 else "failed",
            "exit_code": worktree_code,
        })
        record = build_record(commit, checks, source, run_url)
        write_record_atomically(output, record)
        print(f"Verification evidence: {output} ({record['overall_status']})")
        return 0 if record["overall_status"] == "passed" else 1
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        print(f"verification evidence failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
