# GS Korean -> Pocket Monsters — v9 routing

Canonical project home: `CROSS-GEN/TARGET/GS-KOREAN-TO-POCKET-MONSTERS/`.

The project translates each Japanese source directly from Japanese and each English source directly from English. Official Korean Gold/Silver are both independent language-audit targets and the primary Game Boy Korean implementation references.

## Canonical source grammar

```text
GEN-XX/<GAME-ID>/SOURCE/<PLATFORM-ID>/<PACKAGE-KIND>/<RELEASE-ID>/
```

Exact supplied images are dump observations under the release:

```text
<RELEASE-ID>/DUMPS/<DUMP-ID>/
```

`DUMP-ID` is an opaque existing identity. Historic prefixes such as `USER-UPLOAD-`, `UPLOAD-`, and `PROJECT-` are retained where already established; v9 does not rename a dump merely to make prefixes uniform. Hashes lock the exact image. ROM binaries are never committed.

## Release identity rule

Use the strongest stable technical release identity available. Market/language labels remain canonical only when no stronger technical identifier is established.

Generation II canonical technical IDs in this project include:

```text
Gold:    AAUJ-HV0, AAUJ-HV1, AAUE-HV0, AAUK-HV0
Silver:  AAXJ-HV0, AAXJ-HV1, AAXE-HV0, AAXK-HV0
Crystal: BXTJ-HV0, BYTE-HV0, BYTE-HV1
```

For Crystal, the former language-label source directories are legacy aliases and receive no new work:

```text
JP-JA-HV0     -> BXTJ-HV0
US-EU-EN-HV0  -> BYTE-HV0
US-EU-EN-HV1  -> BYTE-HV1
```

They are retained until references are migrated; they are not independent releases.

Generation I does not expose an equivalent stable product/game code in the source header, so IDs such as `JP-JA-HV0` and `US-EU-EN-HV0` remain canonical release IDs there.

## Platform routing

Platform identity follows the actual cartridge compatibility/header classification used by the repository, not the filename extension alone. In particular, the supplied English Yellow image is canonical under:

```text
GEN-01/YELLOW/SOURCE/GBC/CART/US-EU-EN-HV0/
```

Japanese Yellow revisions remain under `SOURCE/GB/CART/`.

## Target variants

Each distinct source release has an independent Korean target:

```text
KO-<GENERATION>-<GAME>-<RELEASE-ID>
```

There are 23 supplied source releases and therefore 23 buildable target variants in the current matrix. Japanese and English localization differences, plus revision differences, are preserved rather than collapsed into one Korean text set.

## Repository split

**Sakurai** owns release/dump identity, hashes, headers, bank and pointer analysis, text/code reverse engineering, translation crosswalks, relocation/UI/SRAM specifications, reports, tools, and verification evidence.

**Tsubaki** owns verified extracted/normalized production assets, converted resources, insertion/engine implementation data, build inputs, patches, catalogs, and production verification.

A reusable asset may be shared only after byte identity/provenance is verified. The GS Korean Hangul font is one such verified shared production asset; its manifest lists both `AAUK-HV0` and `AAXK-HV0` as sources.

## Authoritative project manifests

- `source-matrix.yaml` — canonical 23-source routing and hashes
- `target-matrix.yaml` — canonical 23-target mapping
- `SOURCE-SET-23.csv` — tabular source/dump/target lock
- `SOURCE-ROM-AUDIT/` and verification reports — observation evidence

No new path under `LIBRARY/`, `PROJECTS/`, `LEGACY/`, `MULTI`, `REV-ALL`, `MISC`, `OTHER`, or `GENERAL` is canonical.
