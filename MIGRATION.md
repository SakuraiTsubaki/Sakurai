# Repository Migration

## Canonical model

The repository follows:

`GENERATION → GAME → LANGUAGE/REGION → REV → WORK TYPE`

Git history is the archive for old paths. The current tree must not keep a second live copy solely to preserve a legacy pathname.

## Semantic normalization

The first canonical migration promoted generation/game/locale/revision/work-type ownership but retained some complete legacy routes below WORK TYPE. Those nested replicas are now considered non-canonical.

Generation IV has completed second-stage semantic normalization:

- legacy bundle/region/revision/work-type replicas were dismantled;
- single-game material was returned to the actual game/locale/revision owner;
- multi-game comparisons were placed under `_SHARED` with the narrowest truthful locale/revision scope;
- mixed Phase 1–3 buckets were split by semantic work type;
- cross-generation studies were normalized under `ANALYSIS/CROSS-GENERATION`;
- old path provenance is preserved in Git history and manifests rather than duplicate live directories.

See `GENERATION-IV/_SHARED/MULTI/REV-ALL/MANIFESTS/PATH-DESIGN.md` for the Generation IV routing rules.

## Validation

`MIGRATED` is forbidden. Generation IV additionally uses strict below-WORK-TYPE validation so locale, revision, work-type and legacy wrapper roles cannot be recreated inside the subject tree.

Other generations retain the canonical five-level ownership model and can be added to strict semantic validation as their remaining legacy subtrees are normalized.
