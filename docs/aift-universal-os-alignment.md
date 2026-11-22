# .github — Proposed Universal AIFT OS Documentation Relationship

> **Informational planning only.** Source architecture and editable infographics appear in [AIFT-OS PR #92](https://github.com/AIFreedomTrustFederation/AIFT-OS/pull/92). All native boot, hosted OS and future physical device support remain separately unverified until exact target evidence exists.

## Current authority

Organization repository catalog, contribution policy and cross-repository authority metadata. Only individual repositories can assert their own implementation state.

## Future relationship

Add an evidence-only reference guide pointing to the proposed AIFT-OS roadmap and future owners for kernel/boot, hosted sessions, UXI, robotics/mobile simulation and release; this is not a change to the current federation.repositories.json authority classifications.

~~~mermaid
flowchart LR
  SOURCE[".github: current source authority"] --> GUIDE["Proposed informational alignment"]
  GUIDE -. "reference only" .-> OS["AIFT-OS architecture under review"]
  EVIDENCE["Per-repository primary evidence"] --> GUIDE
  REVIEW["Owner and publication approvals"] --> GUIDE
~~~

## Documentation acceptance

1. Preserve the existing README, AGENTS, repository catalog and publication boundary.
2. Confirm the central PR is indeed a draft design proposal, not a released firmware or deployed OS.
3. Never confuse GitHub presence, published roadmap or passing documentation CI with installed, booted or safe hardware.
4. Verification needed: Cross-check named repo existence and README/AGENTS provenance; exact-head review of the catalog before *any future* machine-readable change.
5. Do not add secrets, privileged routes, fabricated project achievements, or credentials.

## Restricted changes

Do not recategorize canonical/incubating/upstream-derived repos, modify governance, create an organization-wide policy or assert production support based on a docs link. Follow owner-specific AGENTS instructions. This document grants no new control, release authority, user permissions, device privileges or auto-merge exemptions.
