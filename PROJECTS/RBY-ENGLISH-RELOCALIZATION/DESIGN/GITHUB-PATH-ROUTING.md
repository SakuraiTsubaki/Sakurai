# RBY English Relocalization — canonical GitHub routing

Status: **v4 canonical** (2026-09-12)

## Identity spine

Official source facts and exact supplied files are separated:

```text
LIBRARY/GEN-01/GB/<GAME>/RELEASES/<RELEASE-ID>/
├── MANIFESTS/release.json
└── DUMPS/<DUMP-ID>/MANIFESTS/dump.json
```

For Gen I GB releases, canonical IDs use header-version identity:

- Japanese: `JP-JA-HV0`, `JP-JA-HV1`, etc.
- English USA/Europe: `US-EU-EN-HV0`.
- Preservation labels remain metadata. Japanese Pikachu `Rev 0A/B/C/D` therefore map to `HV0/HV1/HV2/HV3` while preserving the labels explicitly.

## Project routing

```text
PROJECTS/RBY-ENGLISH-RELOCALIZATION/
├── MANIFESTS/
│   ├── source-set.json
│   └── release-lock.json
├── DIFFS/
├── DESIGN/
├── TOOLS/
├── VERIFICATION/
└── REPORTS/
```

Japanese Red/Green/Blue/Pikachu releases are `TRANSLATION-ORIGINAL` + `BUILD-BASE`. Official English Red/Blue/Yellow releases are `IMPLEMENTATION-REFERENCE` only.

Green is an independent translation/build target. No fictitious official English Green release is created.

## Repository split

### Sakurai
Owns release/dump identities, ROM research, revision diffs, text/data analysis, bank/pointer/space ownership analysis, tools, reports, and verification evidence.

### Tsubaki
Owns production-side release lock, build-input matrix, converted/extracted implementation resources, build tools, target-specific implementation roots, patches, and generated outputs.

Both repositories use the same release IDs and target IDs.

## Target IDs

Nine Japanese build targets are fixed:

- `RED-JP-JA-HV0-ENGLISH`
- `RED-JP-JA-HV1-ENGLISH`
- `GREEN-JP-JA-HV0-ENGLISH`
- `GREEN-JP-JA-HV1-ENGLISH`
- `BLUE-JP-JA-HV0-ENGLISH`
- `YELLOW-JP-JA-HV0-ENGLISH`
- `YELLOW-JP-JA-HV1-ENGLISH`
- `YELLOW-JP-JA-HV2-ENGLISH`
- `YELLOW-JP-JA-HV3-ENGLISH`

## Allocation invariant

A long `00` or `FF` run is never considered safe free space merely because it looks empty. It remains an `UNVERIFIED-PADDING-CANDIDATE` until code, pointer, table, graphics, event, and other ownership analysis proves the region safe.

## Legacy retirement

The old v3 `GAMES/GEN-01/.../RBY-ENGLISH-RELOCALIZATION/...` project files are retired after their v4 replacements exist. Git history preserves them; no duplicate live copy is kept.
