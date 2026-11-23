#!/usr/bin/env python3
"""Fail-closed, dependency-free continuity documentation gate."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DIRECTIVE = ROOT / "FEDERATION-PRIME-DIRECTIVE.md"
REQUIRED = (
    "Perpetual Continuity and Preservation",
    "last viable recovery path",
    "default branch",
    "required checks",
    "production",
    "AIFT Federation Automation GitHub App",
)
def main():
    try:
        text = DIRECTIVE.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"BLOCKED: cannot read directive: {exc}", file=sys.stderr)
        return 1
    missing = [phrase for phrase in REQUIRED if phrase.lower() not in text.lower()]
    if missing:
        print(f"BLOCKED: missing continuity policy elements: {missing}", file=sys.stderr)
        return 1
    print("PASS: continuity directive required elements present (documentation-only gate)")
    print("NOTE: This does not verify runtime recovery, branch protections, or production readiness.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
