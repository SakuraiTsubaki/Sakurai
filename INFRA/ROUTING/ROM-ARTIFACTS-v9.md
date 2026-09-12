# ROM Artifact Routing — v9

Status: canonical routing policy for the Sakurai/Tsubaki repository pair.

## Principle

A ROM-derived fact has one semantic owner. Sakurai owns **identity, observation, evidence, reverse-engineering knowledge, specification, and verification**. Tsubaki owns **production catalogs, extracted/normalized/converted assets, implementation, patches, and non-ROM build products**.

ROM images themselves are never committed.

## Canonical release leaf

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

For Korean Generation II:

```text
GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0/
GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0/
```

## Route to Sakurai

| Artifact | Canonical owner/path |
| --- | --- |
| Release identity, hashes | `IDENTITY/` |
| Per-dump observations | `DUMPS/<DUMP-ID>/` |
| ROM headers/indexes | `NATIVE/HEADER/`, `NATIVE/INDEXES/` |
| Code/control-flow research | `NATIVE/CODE/`, `ANALYSIS/` |
| Text tables/encodings/pointers | `NATIVE/TEXT/`, `ANALYSIS/` |
| Maps/events/system tables | `NATIVE/MAPS/`, `NATIVE/DOMAINS/`, `ANALYSIS/` |
| Offset/bank/size/hash observations for assets | `ANALYSIS/<DOMAIN>/` |
| Schemas/specifications | `SPEC/` |
| Reproducible research tools | `TOOLS/` |
| Verification evidence | `VERIFICATION/` |

A secondary disassembly or wiki does not become authoritative merely by being imported. Put secondary source material under `REFERENCE/` or record it in provenance; promote claims to `NATIVE/` or verified `ANALYSIS/` only after direct validation against official software or an inspected source image.

## Route to Tsubaki

Tsubaki paths are referenced from Sakurai evidence, but production data is not duplicated here. Typical counterparts are:

```text
CATALOG/
EXTRACTED/
NORMALIZED/
CONVERTED/
TOOLS/
REPORTS/
VERIFICATION/
```

For metadata-only asset descriptions, use Tsubaki `CATALOG/`, not a generic `ASSETS/` directory.

## pokegold-kr routing

Upstream snapshot used during this cutover:

```text
SakuraiTsubaki/pokegold-kr@801b8bf5dc38d1aac121a68ce61bc707afe08e0c
```

The upstream tree is a WIP disassembly that builds Korean Gold and Silver. Do **not** mirror the repository wholesale into either project. Route by meaning:

- `engine/`, `home/`, `data/`, `maps/`, `constants/`, text-related ASM: secondary reverse-engineering/reference material for Sakurai until ROM-verified.
- `gfx/`, `audio/`, asset conversion inputs/recipes: Tsubaki production material when provenance and redistribution status are acceptable.
- `Makefile`, build helpers and production conversion tools: Tsubaki `TOOLS/` or target `BUILD/`/`IMPLEMENTATION/` as appropriate.
- Documentation and third-party-derived character maps remain reference/provenance material unless independently verified.

Because one upstream worktree can build both Gold and Silver, shared files must not be blindly duplicated into both release leaves. Release-specific observations remain release-owned; genuinely identity-independent reusable material may live under `SHARED/`.

## Gen II Korean font example

ROM observation/evidence:

```text
Sakurai:GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0/ANALYSIS/FONTS/GS-KOREAN-HANGUL-8X16.yaml
Sakurai:GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0/ANALYSIS/FONTS/GS-KOREAN-HANGUL-8X16.yaml
```

Production catalogs:

```text
Tsubaki:GEN-02/GOLD/SOURCE/GBC/CART/AAUK-HV0/CATALOG/FONTS/GS-KOREAN-HANGUL-8X16/manifest.json
Tsubaki:GEN-02/SILVER/SOURCE/GBC/CART/AAXK-HV0/CATALOG/FONTS/GS-KOREAN-HANGUL-8X16/manifest.json
```

## Retired paths

No new work may be added below `LIBRARY/`, `PROJECTS/`, `GENERATION-*`, generic release-level `ASSETS/`, or other pre-v9 roots. Existing unique content must be moved to its canonical semantic owner, references repaired, and the old path removed once empty.
