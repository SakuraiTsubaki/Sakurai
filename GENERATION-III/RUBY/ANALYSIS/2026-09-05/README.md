# Pokémon Ruby ROM census — 2026-09-05

This directory records a reproducible first-pass census of the 13 Pokémon Ruby GBA images supplied to the RUBY project. **No ROM image is stored in this repository.** Only metadata, hashes, comparison results, and tooling are tracked.

## Inventory

| Build | Size | Game code | Header rev | SHA-1 |
|---|---:|---|---:|---|
| Japan | 8 MiB | AXVJ | 0 | `5c5e546720300b99ae45d2aa35c646c8b8ff5c56` |
| English USA | 16 MiB | AXVE | 0 | `f28b6ffc97847e94a6c21a63cacf633ee5c8df1e` |
| English Europe | 16 MiB | AXVE | 1 | `610b96a9c9a7d03d2bafb655e7560ccff1a6d894` |
| English USA/Europe | 16 MiB | AXVE | 2 | `5b64eacf892920518db4ec664e62a086dd5f5bc8` |
| German | 16 MiB | AXVD | 0 | `1c2a53332382e14dab8815e3a6dd81ad89534050` |
| German Rev 1 | 16 MiB | AXVD | 1 | `424740be1fc67a5ddb954794443646e6aeee2c1b` |
| German Debug | 16 MiB | AXVD | 0 | `ca5e3d415c4b47353a73a616878ba833f3648b7a` |
| French | 16 MiB | AXVF | 0 | `a6ee94202bec0641c55d242757e84dc89336d4cb` |
| French Rev 1 | 16 MiB | AXVF | 1 | `ba888dfba231a231cbd60fe228e894b54fb1ed79` |
| Italian | 16 MiB | AXVI | 0 | `2b3134224392f58da00f802faa1bf4b5cf6270be` |
| Italian Rev 1 | 16 MiB | AXVI | 1 | `015a5d380afe316a2a6fcc561798ebff9dfb3009` |
| Spanish | 16 MiB | AXVS | 0 | `1f49f7289253dcbfecbc4c5ba3e67aa0652ec83c` |
| Spanish Rev 1 | 16 MiB | AXVS | 1 | `9ac73481d7f5d150a018309bba91d185ce99fb7c` |

All 13 images have a valid GBA header complement checksum. The title field is `POKEMON RUBY`, Nintendo maker code is `01`, and the fixed-value byte is `0x96` in every image.

## Revision findings

The clean European-language Rev 0 → Rev 1 deltas for German, French, Italian, and Spanish are exactly **4 bytes** each:

- header revision byte `0x000000BC`: `00 → 01`;
- header complement checksum `0x000000BD`: decremented to match the new header;
- two Thumb conditional-branch condition bytes at `0x00009367` and `0x0000938B`: `DD → DB` and `DC → DA`.

English EU Rev 1 → USA/EU Rev 2 has the same 4-byte pattern, but the two code bytes occur at `0x0000919B` and `0x000091BF`; header revision becomes `01 → 02`.

The USA English Rev 0 image and Europe English Rev 1 image are **not a clean 4-byte revision pair**: 5,744,535 bytes differ across 419,998 contiguous ranges. They should therefore be treated as distinct regional/build baselines when doing source provenance, rather than assuming that the EU Rev 1 file is simply the USA Rev 0 ROM plus the four-byte revision patch.

The German Debug build is also a genuinely distinct build: versus German retail Rev 0, 6,751,723 bytes differ across 263,540 ranges. It shares `AXVD` and header revision 0, so filename/header revision alone is insufficient to identify it.

## Padding / occupied extent

The 16 MiB localized builds end in a long `0xFF` suffix beginning around `0x00EAExxx–0x00EB1xxx`, depending on language/build. The Japanese 8 MiB image instead has only a 408-byte terminal `0xFF` suffix beginning at `0x007FFE68`. These are observations, not yet declarations of safe free space: every candidate region still needs pointer/reference and runtime-use verification before patch allocation.

## Files

- `rom_inventory.csv` — flat ROM identity/header/hash ledger.
- `rom_inventory.json` — same ledger in structured form.
- `revision_diff_summary.csv` — first-pass binary pair comparison.
- `ruby_rom_census.py` — reproducible census generator. It reads local `.gba` inputs but never copies ROM data into outputs.

## Next analysis layer

The next exhaustive pass should map ROM regions/banks, code vs. data, text tables, scripts, maps/events, Pokémon/move/item/trainer data, graphics, audio, save structures, and all localization-specific assets, while maintaining per-build provenance and revision deltas.
