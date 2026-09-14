# Migration Audit

The legacy tree is too mixed to migrate safely by moving whole directories. From this point forward, migration is performed at the smallest practical file or subdirectory unit.

## Rule

**Do not move an entire legacy game tree solely because its folder name matches one upstream game.**

Every candidate item must be classified before relocation.

## Required audit fields

For each file or coherent subdirectory, record:

- `legacy_path` — current/previous path in Sakurai
- `source_family` — `disassembly`, `decompilation`, `multiple`, `unknown`
- `source_repository` — exact upstream repository when known
- `source_revision` — commit/tag/ref when known
- `kind` — analysis, source, data, asset, manifest, report, comparison, release identity, tool, test, verification, shared, derived, etc.
- `target` — game/version/region/language/revision/build when known
- `destination` — proposed aggregate path
- `evidence` — why that destination is correct
- `dedup_status` — unique, duplicate-unverified, byte-identical, semantic-equivalent, not-applicable
- `verification` — Unverified / Observed / Reproduced / Matched
- `notes`

## Destination rules

- `projects/disassembly/<REPOSITORY>/...` only for material traceable to one Disassembly upstream repository.
- `projects/decompilation/<REPOSITORY>/...` only for material traceable to one Decompilation upstream repository.
- `shared/...` only after equivalence across multiple upstreams is verified.
- `derived/...` for comparisons, consolidated reports, cross-repository analyses, synthesized inventories, or other work whose owner is the combined corpus.
- Unknown ownership stays in place until evidence is sufficient.

## Re-audit of earlier bulk moves

Generation I and Generation II were initially moved by reusing whole Git tree objects. Those placements are **provisional only** and must be re-audited item by item.

A bulk-moved directory is not considered canonical merely because it now lives under an upstream namespace.

## Audit order

1. Generation I provisional placements
2. Generation II provisional placements
3. Generation III mixed Disassembly/Decompilation material
4. remaining `GEN-*`
5. `CROSS-GEN`
6. remaining `INFRA`

Within each generation, classify direct upstream material first, then shared material, then derived/comparison material.

## Safety

- Preserve Git history; do not rewrite history for migration cleanup.
- Do not delete unique material until its destination has been verified.
- Do not deduplicate by filename, visual similarity, or folder name alone.
- Keep complete playable ROM image files out of GitHub.
