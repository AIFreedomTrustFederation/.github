# AGENTS.md — Federation Catalog and Organization Profile

## Scope

This repository publishes the AIFreedomTrustFederation organization profile and the authoritative repository catalog. Treat `federation.repositories.json` as organization-wide coordination metadata, not as a place to redefine the mission or authority of individual projects.

## Required Behavior

- Keep public claims grounded in evidence from the repository that owns the referenced capability.
- Preserve each project's name, layer, role, runtime, authority, and upstream relationship accurately.
- Do not add a catalog entry without its canonical HTTPS GitHub evidence URL.
- Do not describe conceptual, incubating, overlapping, supporting, or upstream-derived work as canonical.
- Preserve upstream attribution and repository boundaries.
- Never add credentials, private URLs, personal data, or unpublished operational details.

## Human Approval Required

- changing a repository's authority classification or lifecycle status
- removing a repository from the catalog
- changing organization-wide doctrine, governance, security, financial, health, or legal claims
- publishing claims that another repository has not established through its own artifacts or executable evidence

## Validation

Use Python 3.13 and run the same dependency-free, non-mutating catalog gate enforced by CI:

```sh
PYTHONPYCACHEPREFIX="$(mktemp -d)" python -m py_compile scripts/validate_repository_catalog.py
python scripts/validate_repository_catalog.py
git diff --check
test -z "$(git status --porcelain)"
```

If the catalog and public profile both change, verify that their repository names, authority language, and public links remain consistent. Validation must not modify tracked files or leave generated files in the checkout.
