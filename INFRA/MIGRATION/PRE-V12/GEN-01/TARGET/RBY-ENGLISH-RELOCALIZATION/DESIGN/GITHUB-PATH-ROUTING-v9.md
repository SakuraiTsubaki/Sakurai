# GitHub path routing v9 — RBY ENGLISH → ポケットモンスター

Status: **canonical for this project** — 2026-09-13.

## Canonical ownership

- `Sakurai`: source identity, ROM observations, bank fingerprints, comparisons, translation research/specification, audit and verification.
- `Tsubaki`: source locks needed by builders, extracted/normalized production assets, implementation data, patches, build metadata and build verification.
- ROM binaries (`.gb`, `.gbc`, modified full ROM images) are never committed.

## Source ROM paths

```text
GEN-01/<GAME>/SOURCE/<PLATFORM-ID>/CART/<RELEASE-ID>/
```

Platform ID follows the actual release identity, not the project as a whole. Japanese Red/Green/Blue/Yellow and English Red/Blue are routed through `GB`. English Yellow `US-EU-EN-HV0` is routed through `GBC` because its ROM header has CGB flag `0x80`:

```text
GEN-01/YELLOW/SOURCE/GBC/CART/US-EU-EN-HV0/
```

The 12 locked releases used by this project are: RED `JP-JA-HV0`, `JP-JA-HV1`, `US-EU-EN-HV0`; GREEN `JP-JA-HV0`, `JP-JA-HV1`; BLUE `JP-JA-HV0`, `US-EU-EN-HV0`; YELLOW `JP-JA-HV0`..`JP-JA-HV3`, `US-EU-EN-HV0`.

## Project path

Because one target intentionally spans four Generation I games, the project is owned at generation scope:

```text
GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/
```

Do not recreate `PROJECTS/GEN-01/...` or `LIBRARY/GEN-01/...`. Those strings are legacy references only and must be migrated when touched.

## Cross-game research

```text
GEN-01/COMPARE/RBY-ROM-CENSUS-<DATE>/
GEN-01/COMPARE/RBY-TEXT-ENGINE-CENSUS-<DATE>/
```

Game-local revision comparisons remain under `GEN-01/<GAME>/COMPARE/...`.

## Project sections

Sakurai:
```text
GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/
  MANIFESTS/ ANALYSIS/ DESIGN/ TRANSLATION/ REPORTS/ VERIFICATION/ TOOLS/
```

Tsubaki:
```text
GEN-01/TARGET/RBY-ENGLISH-RELOCALIZATION/
  MANIFESTS/ INPUTS/ ASSETS/ NORMALIZED/ CONVERTED/ IMPLEMENTATION/ PATCHES/ BUILD/ CATALOG/ TOOLS/ REPORTS/ VERIFICATION/
```

`SOURCE/` inside the target is deprecated for raw source ownership. Build-facing implementation source lives under `IMPLEMENTATION/`; official release data remains under each game's `SOURCE/`.
