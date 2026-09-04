# Pokémon Green (Japan) — full ROM census, pass 1

Date: 2026-09-05 (Asia/Seoul)

## Scope

First exhaustive structural census of the two project inputs: Pocket Monsters Midori (Japan) Rev 0 and Rev A. ROM binaries are deliberately excluded. Only metadata, hashes, maps, aggregate statistics, decoded text candidates, and reproducible tooling are stored.

## Identity

| Revision | SHA-1 | Size | 16 KiB banks | Header version |
|---|---|---:|---:|---:|
| Rev 0 | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` | 524,288 | 32 | 0 |
| Rev A | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` | 524,288 | 32 | 1 |

Both header and global checksums validate. These hashes exactly match the `Narishma-gb/pokegreen` Rev 0 / Rev 1 disassembly targets, so its linker layout can be used as the semantic ownership reference rather than guessing from byte patterns.

## Critical ROM-capacity finding

Do **not** treat long `00` or `FF` runs as free ROM space. Exact linker maps show:

- Rev 0: ROM0 16,384 used / 0 free; ROMX 507,903 used / **1 free byte**.
- Rev A: ROM0 16,384 used / 0 free; ROMX 507,904 used / **0 free bytes**.
- Rev 0's only linker-unallocated ROM byte is bank `1A`, CPU `$7FFF`, file offset `0x06BFFF`.
- Rev A allocates that byte as `Garbage 26`.

Therefore localization/expansion must assume relocation and/or ROM bank expansion. `fill_runs_*.csv` marks only `padding_or_garbage_candidate`; it is never a safe-space claim.

## Rev 0 ↔ Rev A

- Same-offset differing bytes: **46,168 / 524,288 (8.805847%)**.
- Contiguous raw difference runs: **5,436**.
- Exactly identical bank: **1B**.
- Highest raw deltas: bank `0F` 15,403 bytes, bank `00` 13,109, bank `01` 11,803.
- Sequence-alignment similarity remains 0.902527 / 0.935791 / 0.918396 for those three banks, showing that much of the enormous same-offset delta is shifted/repacked/garbage-sensitive data rather than tens of thousands of independent semantic edits.

The standard cartridge header `0x0100-0x014F` differs only at mask-ROM version (`0x014C`) and the dependent header/global checksum bytes (`0x014D-0x014F`). The `0x0068-0x00FF` region is linker-owned `Garbage Header`, not standard cartridge-header fields.

Among selected reset/interrupt vectors, only Timer changes its jump target: Rev 0 `JP $0D9A` → Rev A `JP $0D88`.

## 32-bank ownership

See `bank_ownership.csv` for the complete matrix. Exact high-level layout:

| Bank | Primary ownership |
|---:|---|
| 00 | Fixed-bank core: reset/interrupts, text engine, graphics transfer, serial/audio dispatch, common routines |
| 01 | Mixed core/data: sprite facings, Pokémon/item data and names, miscellaneous systems |
| 02 | Audio engine/music/SFX set 1 |
| 03 | Input + map/object/event support |
| 04 | Move names, font graphics, Start menu, NPC sprites, battle engine |
| 05 | NPC sprites + battle engine |
| 06 | Maps + play time + doors/ledges |
| 07 | Maps + clear-save + hidden events |
| 08 | Bill's PC + audio engine/music/SFX set 2 |
| 09-0C | Pics + battle engines |
| 0D | Pics + slot machines |
| 0E | Battle engine |
| 0F | Battle core |
| 10 | Pokédex menus + trade movie + mixed routines |
| 11 | Maps + Pokédex rating + hidden-event core |
| 12 | Maps + screen effects |
| 13 | Trainer pics + maps + predefs |
| 14 | Maps + battle engine + hidden events |
| 15 | Maps + battle engine + diploma + trainer sight |
| 16 | Maps + battle engines |
| 17 | Maps + starter Pokédex + hidden events |
| 18 | Maps + fossil lab + hidden events |
| 19 | Tilesets |
| 1A | Version graphics + tilesets + battle engine 12 |
| 1B | Tilesets |
| 1C | Credits/splash/movie + presentation routines |
| 1D | Maps + Itemfinder + vending machine |
| 1E | Status ailments + battle animations + Pokémon/battle systems |
| 1F | Audio engine/music/SFX set 3 |

## Japanese text discovery

Generation I Japanese charmap + `0x50` terminator/control-code-aware scan of Rev 0 found:

- **1,580** terminated Japanese-string candidates
- **23,719** candidate bytes
- **17** same-bank pointer-table candidate runs

This is a discovery index and still allows false positives inside binary/graphics data. Recognizable results include `マスターボール`, `ハイパーボール`, `スーパーボール`, `モンスターボール`, `タウンマップ`, `じてんしゃ`, `ポケモンずかん`, `わざマシン`, `トレーナー`, `パソコン`, `ロケットだん`, and `ポケモン`.

## Memory reference

Exact linker layout also confirms VRAM fully allocated (8 KiB), WRAM0 fully allocated (8 KiB), four SRAM banks for sprite/Hall-of-Fame buffers, save data and boxes 1–8, and HRAM 116 bytes used / 11 free. RAM free counts are not ROM expansion capacity.

## Canonical pass-1 files

- `rom_overview.json` — identity/header/global comparison.
- `bank_ownership.csv` — exact 32-bank semantic ownership + measured statistics.
- `bank_stats.csv` — entropy/population/diff/text-candidate metrics.
- `revision_sequence_alignment_by_bank.csv` — shift-sensitive Rev A similarity.
- `largest_revision_diff_runs.csv` — largest contiguous raw diff regions.
- `vector_revision_comparison.csv` — selected reset/interrupt entry comparison.
- `jp_text_pointer_table_candidates_rev0.csv` — pointer-table discovery index.
- Full text/page/diff/fill discovery indexes are reproducible with `tools/green_full_census.py`; large exhaustive indexes can be generated without storing ROM payload bytes.

## Status

Pass 1 establishes identity, address-space pressure, bank ownership, fixed vectors, byte/page metrics, revision hotspots, and text discovery. The next semantic census binds every concrete symbol/range to map headers/blocks/scripts, NPC/event text, hidden events, trainers, wild encounters, items, Pokémon/base stats/moves, battle routines/messages, Pokédex, graphics/font/title/intro, audio, save structures, unused/garbage, and source-level Rev 0 ↔ Rev A changes.
