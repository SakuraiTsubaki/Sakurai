# FireRed 8-ROM Semantic Census — Stage 5

Scope: full-ROM pointer/reference text candidate graph, font anchor verification, exact flash save-sector serialization, and JP Rev0 high-ROM residual characterization. ROM binaries are not stored in GitHub.

## Validation status

- 8/8 aligned ROM-pointer regression checks match Stage 2 exactly.
- 8/8 all-byte pointer scans partition exactly into source-offset shifts 0/1/2/3.
- Text parser uses FireRed control-byte semantics from `include/characters.h` and `src/text.c` in `pret/pokefirered`.
- Referenced text rows remain **candidates**, not claims that every row is a semantic game string. Arbitrary binary data can occasionally satisfy the encoded-text grammar.

## Pointer/reference text graph

| ROM | all-byte ptr-like refs | aligned refs | unique targets | string candidates | candidates with aligned refs | unaligned-only candidates |
|---|---:|---:|---:|---:|---:|---:|
| Pocket Monsters - Fire Red (Japan) (Rev 1).gba | 143,178 | 63,953 | 75,795 | 18,595 | 12,298 | 6,297 |
| Pocket Monsters - Fire Red (Japan).gba | 144,721 | 64,495 | 75,984 | 18,461 | 11,997 | 6,464 |
| Pokemon - Edicion Rojo Fuego (Spain).gba | 140,276 | 63,563 | 75,619 | 12,610 | 8,103 | 4,507 |
| Pokemon - Feuerrote Edition (Germany).gba | 140,385 | 63,463 | 75,523 | 13,150 | 8,166 | 4,984 |
| Pokemon - Fire Red Version (USA).gba | 141,483 | 63,771 | 75,925 | 12,969 | 8,096 | 4,873 |
| Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba | 141,209 | 63,766 | 75,908 | 13,047 | 8,101 | 4,946 |
| Pokemon - Version Rouge Feu (France).gba | 140,902 | 63,524 | 75,654 | 12,520 | 8,098 | 4,422 |
| Pokemon - Versione Rosso Fuoco (Italy).gba | 140,234 | 63,511 | 75,601 | 12,607 | 8,133 | 4,474 |

The all-byte scan deliberately includes unaligned 32-bit values because event/script bytecode can embed pointers at non-word-aligned source positions. The aligned subset is retained as the direct regression anchor against Stage 2.

## Text control grammar correction

Stage 5 initially used an inaccurate argument-count table for several `0xFC` extended control codes. It has been corrected to the actual FireRed text engine behavior: WAIT_SE=0 args, PLAY_BGM=2, PLAY_SE=2, FILL_WINDOW=0, etc. `CHAR_DYNAMIC`/keypad/extra-symbol families consume one following byte; placeholders consume one id byte.

## Font anchor

A 64-byte prefix from `sFontSmallLatinGlyphWidths` is byte-identical and unique in all six western builds, and absent from both JP builds:

- `Pocket Monsters - Fire Red (Japan) (Rev 1).gba` → no hit (JP layout differs / no shared Latin prefix)
- `Pocket Monsters - Fire Red (Japan).gba` → no hit (JP layout differs / no shared Latin prefix)
- `Pokemon - Edicion Rojo Fuego (Spain).gba` → 0x001EA66C (shared Western small-Latin width prefix)
- `Pokemon - Feuerrote Edition (Germany).gba` → 0x001EEDD0 (shared Western small-Latin width prefix)
- `Pokemon - Fire Red Version (USA).gba` → 0x001EEF00 (shared Western small-Latin width prefix)
- `Pokemon - Fire Red Version (USA, Europe) (Rev 1).gba` → 0x001EEF70 (shared Western small-Latin width prefix)
- `Pokemon - Version Rouge Feu (France).gba` → 0x001E930C (shared Western small-Latin width prefix)
- `Pokemon - Versione Rosso Fuoco (Italy).gba` → 0x001E7FA4 (shared Western small-Latin width prefix)

This is a localization-layout anchor only. It does not imply that the complete Latin width table is identical across all western languages.

## Save serialization

- Flash size: 128 KiB = 32 × 4096-byte sectors.
- Main save slot: 14 sectors; two rotating slots occupy sectors 0–27.
- Special sectors: Hall of Fame 28–29; Trainer Tower 30–31.
- Each normal sector: 3968-byte payload + 128-byte footer.
- Footer offsets: unused `0xF80–0xFF3`, id `0xFF4`, checksum `0xFF6`, signature `0xFF8`, counter `0xFFC`.
- SaveBlock2: 3876 bytes in both JP/western builds.
- SaveBlock1: JP 15680 bytes (`0x3D40`); western 15720 bytes (`0x3D68`).
- Pokémon Storage: 33744 bytes (`0x83D0`).
- Last SaveBlock1 chunk: JP 3776 bytes vs western 3816 bytes; last storage chunk: 2000 bytes.

The exact per-sector offsets/sizes are in `save_sector_layout_exact.csv`. The ROM constant audit records occurrences of sector signature `0x08012025` and special sentinel `0xB39D`; raw occurrence counts are evidence only because short constants may also occur in unrelated data.

## English revision help-system probe

The candidate graph finds the Rev1 `NEXT DATA` help-system text while the corresponding Rev0 probe does not. This matches the source-level `REVISION` conditional in `data/text/help_system.inc`. This is separate from the Stage 4 Pokédex-entry differences.

## JP Rev0 high-ROM residual

- first high-ROM difference: `0x00F3F3E4`
- last high-ROM difference: `0x00FDFFFE`
- analyzed region: `0x00F3F3E4–0x00FDFFFF` (658,460 bytes)
- JP Rev1 corresponding region is 100% `0xFF`.
- JP Rev0 region entropy ≈ 2.2094 bits/byte, with substantial zero/FF content and many address-like values.

Classification remains **structured build residual / unused structured data**. No stronger semantic label (debug dump, save image, executable block, etc.) is assigned without independent evidence.

## Artifacts

- Review-facing summaries and validation CSVs are stored directly.
- The full per-ROM candidate ledgers are high-volume deterministic intermediates and are **not committed**; the scanner regenerates them byte-for-byte from the eight local ROMs.
- Review-facing summaries, compact bank summaries, validation ledgers, and exact system-layout tables are committed. The full 256-bank × 8-ROM matrix is deterministic local output.
- `artifact_manifest.csv` contains byte sizes and SHA-256 hashes for the committed Stage 5 artifacts.
- Reproducer: `fire_red_stage5_census.py` under the FireRed tools path.

## Status

Stage 5 is closed as a validated **candidate/reference census**, not as final semantic labeling of every string. The next semantic pass should walk map/event/script pointer-bearing structures, then audit audio, RFU/Mystery Gift/e-Reader, and final patch-safe free-space ownership.
