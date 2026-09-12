# RBY GitHub ownership routing — v4.1 hardening

Status: canonical clarification for `RBY-ENGLISH-RELOCALIZATION`.

This does **not** replace repository structure v4. It resolves RBY-specific ownership ambiguities discovered by auditing the supplied Japanese Red/Green/Blue/Pikachu and English Red/Blue/Yellow ROMs.

## 1. Source identity

Official release identity lives only under:

`LIBRARY/GEN-01/GB/<GAME-ID>/RELEASES/<RELEASE-ID>/`

The exact observed ROM file is a child dump:

`.../DUMPS/<DUMP-ID>/`

Full ROM binaries are never committed.

## 2. ROM-derived research

Cross-title or cross-release research belongs to Sakurai:

`LIBRARY/GEN-01/GB/_SHARED/COMPARISONS/<COMPARISON-ID>/`

For the supplied RBY set:

`RBY-ROM-CENSUS-2026-09-12`

This owns bank fingerprints, shared-bank groups, revision relationships, padding candidates and similar evidence. It does not own production graphics.

## 3. Official-release production assets

An asset extracted from an official source release is **not project-owned merely because a project uses it**.

- Asset unique to one release -> that release under `Tsubaki/LIBRARY/.../RELEASES/...`.
- Asset proven byte-identical across multiple titles/releases -> a deduplicated bundle under `Tsubaki/LIBRARY/GEN-01/GB/_SHARED/COMPARISONS/<COMMON-ASSET-ID>/`.
- The project then references that canonical library asset through a manifest.

This prevents copies such as fonts/HUD tiles from living permanently under `PROJECTS/.../SOURCE` when their true owner is the original release set.

## 4. Project-owned work

`PROJECTS/RBY-ENGLISH-RELOCALIZATION/` owns only derived work:

- source/release locks and target bindings;
- Japanese -> English translation records;
- engine/UI adaptation specifications;
- converted resources that no longer represent an untouched original asset;
- target-specific implementation;
- patches/build recipes;
- project verification.

## 5. Repository split

### Sakurai
Identity, ROM census, bank/pointer/text research, revision diffs, translation research, design specs, tools and verification evidence.

### Tsubaki
Canonical production assets, deduplicated original-release asset bundles, converted resources, target implementation, build inputs, patches and build verification.

Release IDs and target IDs are identical between both repositories.

## 6. RBY project roles

Japanese Red/Green/Blue/Pikachu: `TRANSLATION-ORIGINAL` + `BUILD-BASE`.

Official English Red/Blue/Yellow: `IMPLEMENTATION-REFERENCE`.

Green remains independent. There is no fabricated official English Green release.

## 7. Space allocation invariant

Long `00`/`FF` runs remain `UNVERIFIED-PADDING-CANDIDATE`. They may not be used for text relocation until pointer/code/table/graphics/map/event ownership has been checked.
