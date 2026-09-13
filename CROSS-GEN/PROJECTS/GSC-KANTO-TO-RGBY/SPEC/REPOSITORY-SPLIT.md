# Repository split — GSC Kanto → RGBY

This project follows the repository-pair invariant defined by v11.

## Tsubaki

**Tsubaki is the complete non-ROM project superset.** Store every eligible project artifact there unless it is an original, modified, rebuilt, or otherwise playable whole-ROM image (or an equivalent lossless whole-ROM payload).

Tsubaki therefore includes all Sakurai-class research/control artifacts plus upstream source/disassembly mirrors, extraction outputs, discrete ROM-derived assets, graphics/audio/data assets, text/localization work, normalized/converted assets, implementation data, patches, build recipes/logs, tools, tests, experiments, reports, and production verification.

Binary files are not excluded merely because they are binary. Discrete non-ROM assets are valid Tsubaki content.

## Sakurai

Sakurai is the curated knowledge/control subset. It stores identity, provenance, hashes, research, reverse engineering, mappings, schemas/specifications, reports, analysis tools, and verification evidence. Production-only assets and build products do not need to be duplicated into Sakurai.

## Pair invariant

For this actively paired project, a newly committed Sakurai research/control artifact is incomplete if no corresponding Tsubaki artifact is expected at the same semantic coordinate, except repository-specific metadata.

## Canonical coordinate

Both repositories use:

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`

Legacy `projects/gscrgby/` and `workspaces/gscrgby/` are migration inputs only.

## Upstream mirror

`SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c` is mirrored into Tsubaki under `UPSTREAM/GEN-02/POKEGOLD-KR/` as a complete tracked non-ROM tree. The sync excludes full ROM image files while retaining source, data, audio, graphics, tools, docs, patches, and other non-ROM assets.
