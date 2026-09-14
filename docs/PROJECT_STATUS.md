# Project Status

**Current repository stage:** Combined Disassembly + Decompilation aggregation tree — active migration

Sakurai is now defined as the curated research/control projection of a **46-repository upstream corpus**:

- 12 Disassembly repositories
- 34 Decompilation repositories

The canonical aggregate namespaces now exist:

- `projects/disassembly/`
- `projects/decompilation/`
- `shared/`
- `derived/`
- `docs/`
- `manifests/`

`manifests/upstream-repositories.json` is the authoritative source-repository registry. The older V-numbered architecture is retired.

Existing `GEN-*`, `CROSS-GEN`, and remaining `INFRA` material is migration input. It is being mapped into the aggregate tree only after upstream or genuine shared/derived ownership is identified.

## Current priorities

- Map existing Sakurai material to exact upstream repositories.
- Import/aggregate research-control material from both source families without losing provenance.
- Preserve target, region, language, revision, and build differences.
- Deduplicate only after equivalence is verified.
- Keep Sakurai and Tsubaki aggregate coordinates aligned.
- Move genuine cross-repository material to `shared/` or `derived/` instead of hiding it under legacy routing trees.
- Reject complete playable ROM images from Git.

## Verification levels

- **Unverified** — proposed or recorded but not independently checked.
- **Observed** — directly supported by a source, target, or extracted observation.
- **Reproduced** — recreated with documented steps or tooling.
- **Matched** — exact expected identity, bytes, hash, or behavior confirmed for the declared scope.

Update this file whenever upstream coverage or aggregate migration state changes.
