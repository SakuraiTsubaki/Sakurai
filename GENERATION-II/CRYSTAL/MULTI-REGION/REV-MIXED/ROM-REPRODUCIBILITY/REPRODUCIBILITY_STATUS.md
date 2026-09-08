# Reproducibility status

## Level definitions

- **L0 — Identity:** exact source filename/size/checksums and header validation.
- **L1 — Full byte coverage:** every byte covered by bank/page manifests with no gaps.
- **L2 — Lossless structural roundtrip:** split into deterministic 16 KiB banks, concatenate, and reproduce the exact source SHA-256.
- **L3 — Semantic/source bridge:** a symbolic source tree is known to build the exact target binary.
- **L4 — Typed regional reconstruction:** regional differences are represented as typed source/data rather than opaque ROM bytes.
- **L5 — 100% owned source map:** every byte belongs to a named code/data/asset source object with no overlap or gaps.
- **L6 — Independent exact rebuild:** the project can generate the target ROM from source/assets and produces the exact verified hash.

## Current state

| Target | L0 | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| JP_REV0 | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ |
| USA-EUROPE_REV0 | ✅ | ✅ | ✅ | ✅* | ◻️ | ◻️ | ◻️ |
| USA-EUROPE_REV1 | ✅ | ✅ | ✅ | ✅* | ◻️ | ◻️ | ◻️ |
| ES_REV0 | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ |
| DE_REV0 | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ |
| FR_REV0 | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ |
| IT_REV0 | ✅ | ✅ | ✅ | ◻️ | ◻️ | ◻️ | ◻️ |

`✅*` means the exact target SHA-1 is an upstream-supported build identity and the bridge is pinned/documented; this environment did not clone/build the upstream tree locally.

## Cross-version alignment discovered

Across all seven supplied ROMs at the same file offsets:

- 9 / 128 banks are byte-identical across **all seven** versions: `30 31 37 3B 3C 3D 4B 4C 7A`.
- 2,799 / 8,192 pages (256 bytes each) are byte-identical across **all seven** versions.
- The remaining 5,393 pages are version-dependent and require finer structural ownership/alignment rather than assuming equal offsets.

These equality results are evidence for shared regions only; unequal pages can still contain mostly shared code/data shifted by localization changes.
