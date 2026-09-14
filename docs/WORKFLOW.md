# Repository Workflow

This document describes the repository-wide research/control workflow for Sakurai. It does not replace project-specific procedures.

## Standard flow

1. **Identify the owner and target.** Resolve the game/project/release/dump coordinate before adding material.
2. **Record provenance.** Preserve source references, hashes, revisions, dates, repository commits, addresses, offsets, symbols, or other evidence needed to reproduce the observation.
3. **Separate fact from hypothesis.** Use the verification vocabulary in `VERIFICATION.md`; do not present inference as an observed fact.
4. **Analyze and normalize.** Produce comparison tables, technical notes, schemas, manifests, scripts, and other research/control outputs.
5. **Cross-check variants.** Compare languages, regions, revisions, updates, and related releases when the research claim depends on them.
6. **Verify reproducibility.** Record commands, tools, hashes, and expected results when a finding can be reproduced.
7. **Pair with Tsubaki when appropriate.** Production assets, implementation material, complete extraction outputs, and other eligible non-ROM artifacts belong in Tsubaki while Sakurai retains the curated evidence/control record.
8. **Update status and roadmap.** Promote findings only when their evidence level actually improves.

## Evidence levels

- **Unverified** — proposed, imported, or recorded but not independently checked.
- **Observed** — directly confirmed in a target, source, or extracted artifact.
- **Reproduced** — repeatable using documented inputs and steps.
- **Matched** — reconstructed/derived output matches the intended target under the documented comparison method.

## Review rules

- Prefer small, reviewable changes.
- Preserve exact identifiers and hashes when available.
- Do not collapse distinct releases or assets without verified equivalence.
- Do not use visual similarity alone as proof of binary identity.
- Do not commit complete playable ROM images.

## Navigation

See `REPOSITORY_OVERVIEW.md` for repository role, `PROJECT_STANDARDS.md` for shared conventions, `RESEARCH_GUIDE.md` for evidence practice, and `PAIRING.md` for the Sakurai/Tsubaki relationship.
