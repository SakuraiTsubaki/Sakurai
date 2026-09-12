# GS Korean → Pocket Monsters — v6 canonical routing

This project spans Generation I and Generation II, so its only canonical project home is:

```text
PROJECTS/CROSS-GEN/GS-KOREAN-TO-POCKET-MONSTERS/
```

Original ROM binaries are never committed.

## Source ownership

Official source facts remain in the release library:

```text
LIBRARY/GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/CART/<RELEASE-ID>/
```

Exact supplied images are dump identities below the release. A project target never creates a fake official Korean source release.

Generation I uses the existing stable market-language-HV release keys. Generation II Gold/Silver use verified technical tokens (`AAU*`, `AAX*`) where supported by the library. Crystal retains the library's current market-language keys while its `BXTJ`/`BYTE` technical tokens remain metadata.

English Yellow belongs to `GEN-01/YELLOW/SOURCE/GB`; `.gbc` and CGB flag `0x80` are compatibility/dump metadata.

## GS Korean implementation reference

Official Korean Gold and Silver are both translation subjects and technical Hangul references:

```text
LIBRARY/GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0/
LIBRARY/GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0/
```

Release-owned bytes stay owned by each release. Equality of banks `0x6C` and `0x78–0x7A` is recorded in `LIBRARY/GEN-02/COMPARE/...`; it does not create `_SHARED`.

## Sakurai project ownership

```text
MANIFESTS/  INPUTS/  CROSSWALK/  ANALYSIS/  DESIGN/
DIFFS/  TOOLS/  REPORTS/  VERIFICATION/
```

Sakurai owns identity locks, reverse engineering, bank/pointer maps, decoded research tables, JP/EN→KO translation crosswalks, relocation/UI/SRAM design, analysis tools, and verification evidence.

## Tsubaki production ownership

The matching Tsubaki project uses the same project ID and target IDs and owns source extraction recipes, release-owned asset representations, normalized/converted resources, target insertion data, patches, build inputs, catalogs, tools, and production verification.

Git history is the archive. Pre-v6 paths are migration inputs only.
