# Federation Repository Ownership Map

This organization-wide map prevents two repositories from silently claiming the same responsibility. It is descriptive, evidence-aware, and versioned alongside the machine-readable catalog.

## Canonical architecture

| Capability | Owning repository | Boundary |
| --- | --- | --- |
| Truth discovery, governance, missions, evidence, APIs | `AIFT-OS` | Does not own rendering, model weights, Wine, publishing, or cloud hosting |
| Schemas, templates, generators and technical genome | `AIFT-Genesis` | Defines contracts; does not operate deployments |
| Repository/build/package coordination | `AIFT-Forge` | Does not replace the AIFT-OS control plane |
| Local model execution | `AIFT-Runtime` | Does not own governance or user experience |
| Immersive Living Federation client | `c-848263` (Mysterion Cortex) | Existing client to evolve and eventually rename; do not create a duplicate client repo |
| Windows application/game compatibility on Android | `mobox` | Upstream-derived Wine/Box64 runtime, not the AIFT operator console |
| Cloud, nodes, deployment, naming and routing | `VPS` | Infrastructure execution under AIFT governance |
| Model artifacts and model cards | `TheMindofAll` | Artifact registry, not inference orchestration |
| Public doctrine and empirical research | `AI-Freedom-Trust` | Public claims remain maturity-labeled |
| Public organization portal | `www.aifreedomtrust.com` | Public doorway, not an application control plane |

## Known overlaps requiring containment

- `booksmith-ai` is the canonical publishing product. `BookSmith-Federation-OS` is a specification/incubator until intentionally consolidated.
- `capital-city-provisions` is the canonical public provisions workflow. `tastycutz` remains private and must not independently redefine the same public product without a consolidation decision.
- `Aether_Coin_biozonecurrency` owns stewardship implementation. `biozone-harmony-boost` is a concept UI incubator.
- `AetherianGovernance` may hold governance research; executable governance belongs to `AIFT-OS`.
- `repo-brainstorm-backend-forge` is an incubator and has no canonical backend authority.

## Upstream-derived repositories

`mobox`, `OpenMontage`, and `chktex` retain their upstream identity and license obligations. Federation integration must use adapters and manifests rather than recasting an upstream project as the federation control plane.

## Creation rule

Before creating or repurposing a repository:

1. Read this catalog.
2. Inspect the candidate repositories and their manifests.
3. Name exactly one canonical owner.
4. Define adapter boundaries for every other participant.
5. Record whether the repository is canonical, supporting, incubating, conceptual, overlapping, or upstream-derived.
6. Keep working, planned, experimental, and symbolic claims distinct.

The machine-readable source is [`federation.repositories.json`](federation.repositories.json).
