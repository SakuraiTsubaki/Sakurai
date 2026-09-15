# Generation VII USUM external PNG cross-check inventory

Status: **supporting evidence only; not authoritative battle-master source.**

## Upstream pin

- repository: `PokeAPI/sprites`
- commit: `2ecb4eeacd5a1718621fc30f12772e3f60d830b9`
- path: `sprites/pokemon/versions/generation-vii/ultra-sun-ultra-moon/`
- observed base render canvas: 128x128 PNG

Every local copy acquired by the project is pinned to this exact upstream commit and has its own SHA-256 in the batch manifest.

## Role of this source

This mirror is used for:

- normal/shiny visual cross-checks;
- external form-identity cross-checks;
- early small-batch PNG pipeline validation;
- detecting obvious visual regressions in later model-derived renders.

It is **not** used as proof of:

- canonical game archive/member number;
- native Gen VII 2D battle-sprite existence;
- battle camera;
- canonical battle pose/frame;
- back-view master;
- Gen III palette or placement.

PokeAPI IDs and filenames are API/mirror identifiers, not game GARC-member indices.

## Back-view limitation

No corresponding `back/` directory was found for this USUM version tree during direct repository inspection. Therefore this mirror cannot by itself satisfy the fixed front/back source requirement.

## Variant directories

The upstream version tree exposes variant branches for normal/shiny and gender variants where supported by the mirror. Their presence is treated as external mirror structure only. A file's existence here does not prove that the game stores a unique model/texture member rather than using an alias, material substitution or another runtime relationship.

## Batch 0001

Tsubaki path:

`derived/generation-07/battle-master-v1/source-png/usum-pokeapi-external-crosscheck/batch-0001/`

Coverage:

- 0722 Rowlet
- 0723 Dartrix
- 0724 Decidueye
- 0725 Litten
- 0726 Torracat
- 0727 Incineroar
- 0728 Popplio
- 0729 Brionne
- 0730 Primarina
- 0731 Pikipek

Each has normal and shiny PNG evidence: 20 files total.

Validation:

- PNG signature checked;
- 128x128 checked;
- per-file SHA-256 recorded;
- upstream repository/commit/path recorded.

## Batch 0002 — form-aware test

Logical roles targeted:

| Source mirror ID | National Dex | Species | Form role |
| ---: | ---: | --- | --- |
| 732 | 732 | Trumbeak | base |
| 733 | 733 | Toucannon | base |
| 734 | 734 | Yungoos | base |
| 735 | 735 | Gumshoos | base |
| 10121 | 735 | Gumshoos | Totem |
| 736 | 736 | Grubbin | base |
| 737 | 737 | Charjabug | base |
| 738 | 738 | Vikavolt | base |
| 10122 | 738 | Vikavolt | Totem |
| 739 | 739 | Crabrawler | base |
| 740 | 740 | Crabominable | base |
| 741 | 741 | Oricorio | Baile Style |
| 10123 | 741 | Oricorio | Pom-Pom Style |
| 10124 | 741 | Oricorio | Pa'u Style |
| 10125 | 741 | Oricorio | Sensu Style |

These identifiers were cross-checked against the PokeAPI data repository before acquisition. Batch 0002 deliberately downloads both normal and shiny for every role and fails if an expected pinned raw file is absent. A successful workflow therefore proves the existence of those exact external files at the pinned revision; it still does not convert the API IDs into game archive indices.

Target Tsubaki path:

`derived/generation-07/battle-master-v1/source-png/usum-pokeapi-external-crosscheck/batch-0002/`

## Dedup rule

No two logical roles are collapsed merely because an external PNG appears identical. First record every logical role. Binary/rendered deduplication is a later cryptographic operation that retains aliases in the manifest.

## Acceptance boundary

These external PNGs remain cross-check evidence even after successful binary acquisition. Final `BATTLE_MASTER_V1` acceptance requires canonical model/texture/material/animation provenance, deterministic battle-view front/back reconstruction, 64x64 visual validation, Gen III palette, 4bpp, compression and the complete fixed-contract manifest/hash package.
