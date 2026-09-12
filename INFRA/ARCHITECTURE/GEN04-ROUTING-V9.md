# Generation IV routing — repository v9

Status: canonical for new Generation IV work, 2026-09-13.

## Source releases currently locked

| Game | Locale | Release | Dump |
|---|---|---|---|
| Diamond | US-EN | `ADAE-HV5` | `LGC-a46233d8` |
| Pearl | US-EN | `APAE-HV5` | `LGC-99083bf1` |
| Platinum | KR-KO | `CPUK-HV0` | `UPLOAD-f811d9c7` |
| HeartGold | KR-KO | `IPKK-HV0` | `UPLOAD-5834fb3a` |
| SoulSilver | KR-KO | `IPGK-HV0` | `UPLOAD-0330e644` |

## Sakurai ownership

```text
GEN-04/<GAME>/SOURCE/NDS-NTR/CART/<RELEASE>/
├── IDENTITY/                         # release facts
├── DUMPS/<DUMP>/
│   ├── IDENTITY/                     # exact source-image identity and hashes
│   ├── HEADER/                       # NDS header observations
│   ├── INDEXES/                      # FAT/FNT/NitroFS/overlay indexes
│   └── VERIFICATION/                 # source-image checks
├── NATIVE/                           # release-level semantic reconstruction
├── ANALYSIS/                         # reverse engineering and findings
├── SPEC/                             # reproducible data-layout contracts
├── TOOLS/                            # release-scoped tools when necessary
├── REPORTS/
└── VERIFICATION/
```

Same-game comparisons use `GEN-04/<GAME>/COMPARE/<ID>/`. Cross-game Generation IV comparisons use `GEN-04/COMPARE/<ID>/`.

## Tsubaki ownership

Tsubaki consumes the exact same release and dump IDs. For each source it owns production manifests, catalogs, reproducible extraction/conversion recipes, normalized assets and implementation material. A Tsubaki source manifest references Sakurai with `Sakurai:GEN-04/...`; retired `LIBRARY/...` references are forbidden.

## Migration rules

- `GENERATION-IV/...`, top-level `LIBRARY/...`, and `GEN-04/GENERATION-IV/...` are not destinations for new work.
- Unique historical material is mapped to its semantic game/release/compare/target owner before retirement or quarantine.
- Path aliases never become new release IDs.
- Original or modified `.nds` images are never committed. Exact local inputs are locked by hashes and dump IDs.
- Unknown region/language/revision state stays in manifests; do not create vague `MULTI`, `GENERAL`, `OTHER`, `REV-UNKNOWN`, or `ALL` owners.

## Generation IV cross-game work

D/P/Pt and HG/SS stay game-owned for release data. Engine-wide research that genuinely compares multiple Generation IV titles belongs under `GEN-04/COMPARE/<COMPARISON-ID>/`. A production target spanning all five games belongs under `GEN-04/TARGET/<TARGET-ID>/`; it is not `CROSS-GEN` unless another generation is intentionally part of that same target.
