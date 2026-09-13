# RGBYGSC Kanto Start — source ROM audit

Audit date: 2026-09-13

All supplied Generation I/II project images were read directly from the local project files. No ROM image is stored in GitHub.

## Corpus

- File observations: **16**
- Unique byte images after exact-hash deduplication: **15**
- Games: RED, GREEN, BLUE, YELLOW, GOLD, SILVER, CRYSTAL
- Header checksum valid: **16/16**
- Global checksum valid: **16/16**
- Unique-dump 16 KiB bank observations: **1,248**
- File-observation bank count if the duplicate English Yellow filename is counted twice: **1,312**
- Exact 16 KiB bank hash groups occurring in more than one dump: **235**
- Long `$00`/`$FF` runs of at least 128 bytes across unique dumps: **1,247**

The two supplied English Yellow filenames are byte-identical and map to one v10 dump ID: `DUMP-SHA256-8CBAA499397E4F1A`.

## Korean Silver runtime anchor

- Release: `AAXK-HV0`
- Dump: `DUMP-SHA256-EBBAC63C0C4309C8`
- Full SHA-256: `ebbac63c0c4309c82dbb6723e7163369784f962b4fd3e2f486075307c3008a22`
- Size: 2 MiB
- 16 KiB banks: **128**
- Long `$00`/`$FF` runs >= 128 bytes: **140**
- Sum of those run lengths: **900,460 bytes**
- Completely `$00`-filled 16 KiB banks observed: **24**

Observed byte-blank bank numbers:

`19, 34, 39, 40, 41, 44, 45, 47, 52, 53, 88, 99, 103, 106, 107, 111, 115, 116, 117, 118, 119, 124, 125, 126`

These are **space candidates, not allocation approval**. The project rule remains: before allocating an apparently empty bank, verify pointer tables, bank-switch references, implicit engine assumptions and any data that may be addressed without obvious byte-local references. Only after that verification may a bank be registered for expansion.

## Repository routing

Sakurai stores the evidence and reasoning behind these observations. Tsubaki stores the generated production catalogs and later map/tileset/sprite/text/event/audio/table assets and conversions. The canonical v10 project coordinate in both repositories is:

`CROSS-GEN/PROJECTS/RGBYGSC-KANTO-START/`
