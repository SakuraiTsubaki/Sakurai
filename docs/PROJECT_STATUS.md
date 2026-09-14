# Project Status

**Current repository stage:** Decompilation-aligned operating tree — active migration

Sakurai now uses root-level `docs/` and `manifests/` as its repository-wide operating layer, matching the convention used by the Decompilation series. The older V12 architecture is no longer the repository-wide canonical model.

Generation, cross-generation, and remaining infrastructure content are being simplified separately without deleting unique research material.

## Current priorities

- Keep the root operating layer consistent with the Decompilation repository family.
- Maintain stable target identity, provenance, hashes, research, comparisons, and verification evidence.
- Preserve region/language/revision differences rather than flattening them.
- Keep Sakurai and Tsubaki semantic coordinates aligned.
- Move legacy routing metadata only when its new owner is clear.
- Reject complete playable ROM images from Git.

## Verification levels

- **Unverified** — proposed or recorded but not independently checked.
- **Observed** — directly supported by a source, target, or extracted observation.
- **Reproduced** — recreated with documented steps or tooling.
- **Matched** — exact expected identity, bytes, hash, or behavior confirmed for the declared scope.

Update this file whenever the repository-wide operating model or major migration state changes.
