# Pokémon Sapphire ROM census — 2026-09-05

This directory records a reproducible first-pass census of the 9 Pokémon Sapphire GBA images supplied to the SAPPHIRE project. **No ROM image is stored in this repository.** Only metadata, hashes, comparison results, and tooling are tracked.

## Inventory

| Language | Rev | Game code | Size | SHA-1 | Header | File |
|---|---:|---|---:|---|---|---|
| Japanese | 0 | `AXPJ` | 8.0 MiB | `3233342c2f3087e6ffe6c1791cd5867db07df842` | OK | `Pocket Monsters - Sapphire (Japan).gba` |
| German | 1 | `AXPD` | 16.0 MiB | `7e6e034f9cdca6d2c4a270fdb50a94def5883d17` | OK | `Pokemon - Saphir-Edition (Germany) (Rev 1).gba` |
| English | 1 | `AXPE` | 16.0 MiB | `4722efb8cd45772ca32555b98fd3b9719f8e60a9` | OK | `Pokemon - Sapphire Version (Europe) (Rev 1).gba` |
| English | 0 | `AXPE` | 16.0 MiB | `3ccbbd45f8553c36463f13b938e833f652b793e4` | OK | `Pokemon - Sapphire Version (USA).gba` |
| English | 2 | `AXPE` | 16.0 MiB | `89b45fb172e6b55d51fc0e61989775187f6fe63c` | OK | `Pokemon - Sapphire Version (USA, Europe) (Rev 2).gba` |
| French | 1 | `AXPF` | 16.0 MiB | `860e93f5ea44f4278132f6c1ee5650d07b852fd8` | OK | `Pokemon - Version Saphir (France) (Rev 1).gba` |
| French | 0 | `AXPF` | 16.0 MiB | `c269b5692b2d0e5800ba1ddf117fda95ac648634` | OK | `Pokemon - Version Saphir (France).gba` |
| Italian | 1 | `AXPI` | 16.0 MiB | `73edf67b9b82ff12795622dca412733755d2c0fe` | OK | `Pokemon - Versione Zaffiro (Italy) (Rev 1).gba` |
| Italian | 0 | `AXPI` | 16.0 MiB | `f729dd571fb2c09e72c5c1d68fe0a21e72713d34` | OK | `Pokemon - Versione Zaffiro (Italy).gba` |

## Immediate findings

- All 9 dumps have valid GBA header complement checksums.
- Their Nintendo-logo header block is identical (`SHA-1 17daa0fec02fc33c0f6abb549a8b80b6613b48ee`).
- All 9 contain `FLASH1M_V103`, consistent with the same 1 Mbit flash-save library family.
- Japanese Rev 0 is 8 MiB; all uploaded Western builds are 16 MiB.
- English contains header revisions 0, 1, and 2; French and Italian contain 0 and 1; German currently contains only Rev 1; Japanese currently contains only Rev 0.
- External SHA-1 cross-checks match known clean-retail identities for every uploaded file. The current project set does not include German Rev 0, Japanese Rev 1, or either Spanish retail revision from the commonly indexed set.

## Revision findings

English EU Rev 1 → USA/EU Rev 2, French Rev 0 → Rev 1, and Italian Rev 0 → Rev 1 are each exactly **4 bytes** different:

- header revision/checksum bytes at `0x000000BC–0x000000BD`;
- two Thumb conditional-branch condition bytes.

For English Rev 1 → Rev 2, code bytes are at `0x0000919B` and `0x000091BF`. For French/Italian Rev 0 → Rev 1 they are at `0x00009367` and `0x0000938B`.

At instruction level the conditions change **`BLE → BLT`** and **`BGT → BGE`**, i.e. a real boundary-condition correction. The exact gameplay/system routine should be named only after symbol/address mapping; this census deliberately does not guess its semantic purpose.

English USA Rev 0 → Europe Rev 1 is a completely different kind of comparison: **5,638,997 bytes differ across 377,087 contiguous runs**, with the last difference at `0x00EA79CE`. It must be treated as a distinct regional/build baseline rather than as the Rev 0 image plus the four-byte retail patch.

## Padding / candidate expansion tails

| Build | Trailing `0xFF` bytes | Start |
|---|---:|---:|
| Japanese Rev 0 | 408 | `0x007FFE68` |
| German Rev 1 | 1,372,168 | `0x00EB0FF8` |
| English Rev 0/1/2 | 1,383,440 | `0x00EAE3F0` |
| French Rev 0/1 | 1,371,552 | `0x00EB1260` |
| Italian Rev 0/1 | 1,371,948 | `0x00EB10D4` |

These tails are **padding candidates only**. They are not yet declared safe free space; pointer/reference and runtime-access checks are required first.

## Files

- `rom_inventory.csv` — flat ROM identity/header/hash ledger.
- `revision_diff_summary.csv` — adjacent-revision byte comparison summary.
- `sapphire_rom_census.py` — reproducible census generator; reads local `.gba` files but never copies ROM data into outputs.

## Next exhaustive layer

Map code/data regions, pointer/reference graphs, safe free space, text engine/character tables/fonts/UI, names/Pokédex/scripts/events/battle/system text, graphics/tiles/palettes/sprites, maps/encounters/trainers/items, audio, save/RTC routines, and cross-language symbol/table alignment. Raw offsets must be tied to function/table identity before any cross-build porting.

## External identity cross-check

- `pret/pokeruby` publishes the US Sapphire Rev 0 SHA-1 used by its matching disassembly build.
- `40Cakes/pokebot-gen3` indexes the uploaded Japanese, English, German, French, and Italian SHA-1 values and their retail revision labels.
