#!/usr/bin/env python3
"""Validate the federation repository catalog using only the standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "federation.repositories.json"
EXPECTED_SCHEMA = "aift.repository-catalog.v1"
EXPECTED_AUTHORITY = "AIFreedomTrustFederation/.github"
ALLOWED_AUTHORITIES = {
    "canonical",
    "supporting",
    "incubating",
    "conceptual",
    "overlapping",
    "upstream-derived",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require_text(record: dict[str, object], field: str, name: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(f"{name}: {field} must be a non-empty string")
    return value


def validate() -> int:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schema") != EXPECTED_SCHEMA:
        fail(f"schema must be {EXPECTED_SCHEMA!r}")
    if data.get("authority") != EXPECTED_AUTHORITY:
        fail(f"authority must be {EXPECTED_AUTHORITY!r}")

    vocabulary = data.get("authority_vocabulary")
    if not isinstance(vocabulary, dict) or set(vocabulary) != ALLOWED_AUTHORITIES:
        fail("authority_vocabulary must define exactly the supported authority values")

    repositories = data.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        fail("repositories must be a non-empty list")

    seen_names: set[str] = set()
    seen_evidence: set[str] = set()
    upstream_count = 0
    for index, record in enumerate(repositories):
        if not isinstance(record, dict):
            fail(f"repositories[{index}] must be an object")
        name = require_text(record, "name", f"repositories[{index}]")
        if name in seen_names:
            fail(f"duplicate repository name: {name}")
        seen_names.add(name)

        for field in ("layer", "role", "runtime"):
            require_text(record, field, name)
        authority = require_text(record, "authority", name)
        if authority not in ALLOWED_AUTHORITIES:
            fail(f"{name}: unsupported authority {authority!r}")

        upstream = record.get("upstream")
        if authority == "upstream-derived":
            upstream_count += 1
            if not isinstance(upstream, str) or not upstream.strip():
                fail(f"{name}: upstream-derived entries require an upstream identifier")
        elif upstream is not None:
            fail(f"{name}: upstream is only valid for upstream-derived entries")

        evidence = record.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            fail(f"{name}: evidence must be a non-empty list")
        canonical_url = f"https://github.com/AIFreedomTrustFederation/{name}"
        if canonical_url not in evidence:
            fail(f"{name}: evidence must include {canonical_url}")
        for url in evidence:
            if not isinstance(url, str):
                fail(f"{name}: evidence URLs must be strings")
            parsed = urlparse(url)
            if parsed.scheme != "https" or parsed.netloc != "github.com":
                fail(f"{name}: evidence must use an HTTPS github.com URL")
            if url in seen_evidence:
                fail(f"duplicate evidence URL: {url}")
            seen_evidence.add(url)

    census = data.get("census")
    if not isinstance(census, dict) or census.get("organization") != "AIFreedomTrustFederation":
        fail("census.organization must identify AIFreedomTrustFederation")

    print(
        f"Validated {len(repositories)} federation repositories "
        f"({upstream_count} upstream-derived) in {CATALOG.name}."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(validate())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"catalog validation failed: {error}", file=sys.stderr)
        sys.exit(1)
