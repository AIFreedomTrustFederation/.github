# AIFT Universal OS — Cross-Repository Documentation Review Index

> **Review index, not a release or permission policy.** It tracks proposed, documentation-only integration across all 22 accessible federation repositories. Each repository remains its own implementation source of truth. Do not treat a PR, diagram, reference or passing docs CI as proof of a hardware boot, installed operating system, hosted production session, approved robot, or supported phone.

## Central architecture package

[AIFT-OS draft PR #92](https://github.com/AIFreedomTrustFederation/AIFT-OS/pull/92) includes native Linux/UEFI/QEMU, safe Windows-class PC and separate Intel Mac/Apple Silicon boot paths, hosted sessions, immersive desktop, future phones/robots, exact-head acceptance, governance/permission limits, and **three accessible, editable SVG infographics** for platform layers, boot/device compatibility and portable embodied intelligence with independent safety.

### Proposed delivery and dependency flow

~~~mermaid
flowchart TD
  A["Architecture source: AIFT-OS #92"] --> I["Core interface consumers: Runtime, Forge, VPS"]
  A --> UX["Public Living Universe / Cortex / mobile experience"]
  A --> G["Genesis / governance / doctrine research review"]
  I --> APPS["Publishing, economy, ecology and commerce app boundaries"]
  UX --> APPS
  G --> R["Independent owner / high-risk review"]
  APPS --> R
  R --> E["Only then: verified integration milestones and separately approved release"]
~~~

## Repository documentation proposals

| Repository | Scope | Proposed documentation change | Delivery |
|---|---|---|---|
| AIFT-OS | Core platform + infographic source | [PR #92](https://github.com/AIFreedomTrustFederation/AIFT-OS/pull/92) | Draft |
| AIFT-Runtime | Host service / capability contracts | [PR #16](https://github.com/AIFreedomTrustFederation/AIFT-Runtime/pull/16) | Draft |
| AIFT-Forge | App/agent SDK and manifests | [PR #17](https://github.com/AIFreedomTrustFederation/AIFT-Forge/pull/17) | Draft |
| VPS | Hosted session and release boundaries | [PR #20](https://github.com/AIFreedomTrustFederation/VPS/pull/20) | Draft |
| www.aifreedomtrust.com | Public Tree versus actual OS desktop | [PR #50](https://github.com/AIFreedomTrustFederation/www.aifreedomtrust.com/pull/50) | Draft |
| AIFT-Genesis | Tree/schema ownership and lineage | [PR #10](https://github.com/AIFreedomTrustFederation/AIFT-Genesis/pull/10) | Draft |
| AI-Freedom-Trust | Doctrine/research vs technical evidence | [PR #16](https://github.com/AIFreedomTrustFederation/AI-Freedom-Trust/pull/16) | Draft |
| AetherianGovernance | Consent, governance and privilege boundaries | [PR #2](https://github.com/AIFreedomTrustFederation/AetherianGovernance/pull/2) | Draft |
| TheMindofAll | Models/memory and local AI provenance | [PR #7](https://github.com/AIFreedomTrustFederation/TheMindofAll/pull/7) | Draft |
| mobox | Upstream Android/Termux compatibility | [PR #2](https://github.com/AIFreedomTrustFederation/mobox/pull/2) | Draft; integration under federation/ |
| BookSmith-Federation-OS | Publishing workspace app | [PR #5](https://github.com/AIFreedomTrustFederation/BookSmith-Federation-OS/pull/5) | Draft |
| booksmith-ai | Author-owned real library application | [main commit](https://github.com/AIFreedomTrustFederation/booksmith-ai/commit/71a86f346cb1e19eb5632163c19ee2d148df7621) | Documentation-only direct main following repo instructions |
| Aether_Coin_biozonecurrency | Wallet/issuance authority preserved | [PR #10](https://github.com/AIFreedomTrustFederation/Aether_Coin_biozonecurrency/pull/10) | Draft |
| biozone-harmony-boost | Ecology/wellness optional app | [PR #5](https://github.com/AIFreedomTrustFederation/biozone-harmony-boost/pull/5) | Draft |
| capital-city-provisions | Independent customer/operations app | [PR #8](https://github.com/AIFreedomTrustFederation/capital-city-provisions/pull/8) | Draft |
| tastycutz | Independent commerce app | [PR #5](https://github.com/AIFreedomTrustFederation/tastycutz/pull/5) | Draft |
| .github | Organization catalog boundary | [PR #12](https://github.com/AIFreedomTrustFederation/.github/pull/12) | Draft |
| aifreedomtrustfederation.github.io | Public route index | [PR #4](https://github.com/AIFreedomTrustFederation/aifreedomtrustfederation.github.io/pull/4) | Draft |
| c-848263 | Source-backed experience mapping | [PR #6](https://github.com/AIFreedomTrustFederation/c-848263/pull/6) | Draft |
| repo-brainstorm-backend-forge | Independent app prototype | [PR #4](https://github.com/AIFreedomTrustFederation/repo-brainstorm-backend-forge/pull/4) | Draft |
| OpenMontage | Upstream AI video production app | [PR #3](https://github.com/AIFreedomTrustFederation/OpenMontage/pull/3) | Draft; retain authoritative pipeline |
| chktex | Upstream LaTeX linter/build utility | [PR #1](https://github.com/AIFreedomTrustFederation/chktex/pull/1) | Draft; retain GNU GPL and README |

Links identify **proposals**, not accepted ownership transfers, merged implementations or verified compatibility.

## Review order and source-of-truth protection

1. Review AIFT-OS architecture and diagrams. Check that proposed milestones and safety boundaries are not presented as shipped.
2. Verify Runtime/Forge/VPS integration contracts independently, without introducing public host privileges.
3. Review Living Universe, Genesis and experience docs without misidentifying repositories as fruits or changing canonical doctrine.
4. Have owners of governance, wallet, publishing, commerce, media and upstream-derived tools approve only their own optional, narrowly scoped descriptions. No silent authority reassignment.
5. Verify project-specific AGENTS and tests. Check exact-head Actions, diffs and links separately for each PR; do not infer a single cross-repo green status.
6. Merge only under repository-specific authorization and protections. **No merges or deployment are part of this documentation wave.**

## Release and hardware restrictions

Physical firmware, disk partitioning, BIOS/UEFI replacement, Windows Boot Manager, Intel Mac T2 policy, Apple Silicon boot policy, Android phone unlocking, robot movement, safety controller flashing, production release, signing, identity/governance, financial custody, manuscripts and customer data are all **outside unattended documentation change authority**.

Milestone statuses remain UNVERIFIED until actual target images, QEMU traces, device-specific evidence, application/session behavior and independent physical safety/release requirements have passed.

## Maintenance

Use this file as a review navigation aid, not the source of technical maturity. Future updates should compare exact live PR state before asserting current draft/merged status. The authoritative integration contracts belong to each producer repository; the AIFT-OS platform roadmap defines cross-subsystem targets without absorbing those owners.
