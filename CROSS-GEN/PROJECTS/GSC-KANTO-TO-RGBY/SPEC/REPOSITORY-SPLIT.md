# Repository split — GSC Kanto → RGBY

This project follows the repository-pair invariant defined by v11.

## Tsubaki

**Tsubaki is the complete non-ROM project superset.** Store every eligible project artifact there unless it is an original, modified, rebuilt, or otherwise playable whole-ROM image (or an equivalent lossless whole-ROM payload).

Tsubaki therefore includes all Sakurai-class research/control artifacts plus source/disassembly trees, extraction outputs, discrete ROM-derived assets, graphics/audio/data assets, text/localization work, normalized/converted assets, implementation data, patches, build recipes/logs, tools, tests, experiments, reports, and production verification.

Binary files are not excluded merely because they are binary. Discrete non-ROM assets are valid Tsubaki content.

## Source ownership without duplication

A reusable source project is stored once at its narrowest semantic owner and referenced by larger projects.

For Korean Gold/Silver, the canonical complete non-ROM source tree is:

`Tsubaki:GEN-02/PROJECTS/POKEGOLD-KR/IMPLEMENTATION/`

It is an exact Git-tree match for `SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c`:

- upstream/source tree SHA: `fe50ec090dbf514da2aaa80f331ceedbb30f3197`
- tracked non-ROM files: **4,126**
- tracked ROM files excluded: **0**

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/` references that Generation II source project rather than storing a second copy of the same 4,126 files.

## Sakurai

Sakurai is the curated knowledge/control subset. It stores identity, provenance, hashes, research, reverse engineering, mappings, schemas/specifications, reports, analysis tools, and verification evidence. Production-only assets and build products do not need to be duplicated into Sakurai.

## Pair invariant

For this actively paired project, a newly committed Sakurai research/control artifact is incomplete if no corresponding Tsubaki artifact is expected at the same semantic coordinate, except repository-specific metadata.

## Canonical project coordinate

Both repositories use:

`CROSS-GEN/PROJECTS/GSC-KANTO-TO-RGBY/`

Legacy `projects/gscrgby/` and `workspaces/gscrgby/` are migration inputs only.
