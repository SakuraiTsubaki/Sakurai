# Pokémon Silver Multi-Region Full ROM Census

This directory records the byte/bank-level census of the eight project Silver ROMs. ROM images themselves are not stored here.

## Scope

Targets: JP Rev0, JP RevA, EN, DE, FR, IT, ES, KR.

The census covers ROM identity/integrity, 16 KiB bank atlas, entropy/fill metrics, full-zero/free-bank inventory, uniform slack runs, exact bank identity, aligned localization similarity, 256-byte exact chunk retention, Western text-code candidates, and JP Rev0↔RevA binary differentials.

## Integrity and identity

All eight ROMs pass Nintendo-logo, header-checksum and global-checksum validation. All use cartridge type `0x10` (MBC3 + TIMER + RAM + BATTERY) and declare 32 KiB external RAM.

SHA-1:

| Build | SHA-1 |
|---|---|
| JP Rev0 | `fa8c51059c1642faa570db56ef089f54d1d2011f` |
| JP RevA | `a11d5ddc26eb826086593f82370b15d16404d33e` |
| EN | `49b163f7e57702bc939d642a18f591de55d92dae` |
| DE | `8ecc58d621faaedf2a934bd2583d527220df7bb9` |
| FR | `a4a7e8079b7a53e4d9ef43382bbb1090b9d45d1a` |
| IT | `c9eca9d0a837beb9137bb7d779e469c54e9f8d77` |
| ES | `05bd978ab2cb104b0aff3f696896e30885203a18` |
| KR | `cb22d7e03a74dc3a563fde6be8626626b2b392e7` |

These hashes match the corresponding public disassembly targets/reference records used for cross-checking.

## Architecture

JP is 1 MiB / 64 banks (`00`–`3F`) and packs map scripts into the lower bank range. The Western builds and KR are 2 MiB / 128 banks (`00`–`7F`).

The EN layout uses `40` for standard scripts, `41` for phone scripts, `42`–`62` (with gaps) for map scripts, `64`–`66` for general text, `68`–`6B` for Pokédex entries, `6C` names, `6D` move descriptions, `6E` item descriptions, and `70` for mixed late data/graphics/credits strings.

KR has a distinct high-bank subsystem: `68`/`69` hold the Pokédex halves; `71` contains Hangul structure tables, naming-screen Hangul assets and composition/name-entry code; `72` contains the non-CGB error screen; `78`–`7A` are Hangul tables; `7B` contains diploma graphics. Its header also differs (`CGB 0xC0`, `SGB 0x00`) from JP/Western (`0x80`, `0x03`).

## Exact shared banks

Across all eight ROMs, seven nontrivial aligned banks are byte-for-byte identical:

`0C 2A 30 37 3B 3C 3D`

Using EN labels: Tileset Data 4, Map Blocks 1, Sprites 1, Map Blocks 3/Tileset Data 5, Songs 2, Songs 3/SFX/Cries, Songs 4.

Across the five Western ROMs there are 21 exact non-zero banks:

`0C 12 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 2A 2B 30 37 3B 3C 3D`

## Localization expansion: banks 27 and 58

EN leaves banks `27` and `58` completely zero. DE/FR/IT/ES occupy both.

Bank `27` decodes as localized landmark/location-name data. Examples include ES `PUEBLO PRIMAVERA`, DE `NEUBORKIA`, FR `BOURG GEON`, and IT `BORGO FOGLIANOVA`; only roughly 9–10% of the bank is occupied.

Bank `58` contains localized map dialogue/scripts, including Ruins of Alph / Route 32 gate material. This establishes that the four European localizations use real overflow/split banks rather than being byte-layout clones of EN.

## Full-zero banks

- EN: 28 banks / 458,752 bytes.
- DE/FR/IT/ES: 26 banks / 425,984 bytes each.
- KR: 24 banks / 393,216 bytes.
- JP Rev0/RevA: no completely zero banks.

See `full_zero_banks.csv` for exact bank lists. These are strong free-space candidates, but future allocation must still verify all bank-number assumptions and references.

## JP Rev0 → RevA

The two Japanese ROMs differ at 19,150 byte positions (1.826286% of 1 MiB). Only 16/64 banks differ; 48 are identical.

The apparent large delta is mostly relocation/padding fallout, not 19 KiB of changed game logic. The substantive RevA code change is in bank `23`, in `_InitSpriteAnimStruct`: after incrementing `wSpriteAnimCount`, RevA checks for zero and increments once more so index zero is skipped. The routine grows by five bytes, shifting later bank-23 symbols and low-byte references. Rev0-only garbage/padding accounts for much of the remaining binary difference; bank `3F` in particular is dominated by Rev0 nonzero garbage becoming zero in RevA.

See `jp_rev0_vs_reva_bank_diffs.csv` for the complete per-bank differential census.

## Reproducibility

`full_census.py` regenerates the detailed row-level outputs from the project ROMs. `OUTPUT_MANIFEST.sha256` records SHA-256 hashes for all generated CSV/report/script artifacts. Large row-level CSVs are generated deterministically by the script and retained in the project analysis workspace; summary ledgers are versioned here for direct review.

ROM files are intentionally excluded from version control.