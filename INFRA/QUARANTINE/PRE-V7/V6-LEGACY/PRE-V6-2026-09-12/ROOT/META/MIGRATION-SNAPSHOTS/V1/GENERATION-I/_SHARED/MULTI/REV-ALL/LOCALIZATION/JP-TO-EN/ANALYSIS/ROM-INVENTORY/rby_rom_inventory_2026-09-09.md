# RBY ROM inventory — 2026-09-09

Uploaded ROMs are treated as read-only source/reference binaries. This report contains identifiers and structural metadata only; ROM binaries are not included.

## Inventory

| Role | ROM | Size | Header ver. | Mapper | Region | CGB | SGB | Header/global checksum | SHA-1 |
|---|---|---:|---:|---|---|---|---|---|---|
| JP target base candidate | `Pocket Monsters - Aka (Japan) (Rev A) (SGB Enhanced).gb` | 512 KiB | 1 | MBC1+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `ef74c79cded14204ac79e77f4964d9cb25003120` |
| JP revision reference | `Pocket Monsters - Aka (Japan) (SGB Enhanced).gb` | 512 KiB | 0 | MBC1+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `0623ad12f48c259447980d68bd85ddbf8204b2cd` |
| JP target base candidate | `Pocket Monsters - Ao (Japan) (SGB Enhanced).gb` | 512 KiB | 0 | MBC1+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `0da501e3e5c51ab8fef55b092dcdd7e6b050e424` |
| JP target base candidate | `Pocket Monsters - Midori (Japan) (Rev A) (SGB Enhanced).gb` | 512 KiB | 1 | MBC1+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `4b97cd44aa3f0dd290bfe7b3ac17b7bd8270897b` |
| JP revision reference | `Pocket Monsters - Midori (Japan) (SGB Enhanced).gb` | 512 KiB | 0 | MBC1+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `82c0eef40a5e2423699d9fd8ba15dfaa8b51d196` |
| JP revision reference | `Pocket Monsters - Pikachu (Japan) (Rev 0A) (SGB Enhanced).gb` | 1024 KiB | 0 | MBC3+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `1fb6c264e950d97ce3fd99b347e485b2150df4ff` |
| JP revision reference | `Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb` | 1024 KiB | 1 | MBC3+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `28e4b8531ea4ea1de5a396fccb0cfba51b06b149` |
| JP revision reference | `Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb` | 1024 KiB | 2 | MBC3+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `91864ecdf26d1c593bde4d9ed615520eb57d5e41` |
| JP target base candidate | `Pocket Monsters - Pikachu (Japan) (Rev D) (SGB Enhanced).gb` | 1024 KiB | 3 | MBC3+RAM+BATTERY | Japan | 0x00 | 0x03 | OK | `a40298a8123613ee60cd7aab204d788b8425976e` |
| EN implementation reference | `Pokemon - Blue Version (USA, Europe) (SGB Enhanced).gb` | 1024 KiB | 0 | MBC3+RAM+BATTERY | Non-Japan | 0x00 | 0x03 | OK | `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2` |
| EN implementation reference | `Pokemon - Red Version (USA, Europe) (SGB Enhanced).gb` | 1024 KiB | 0 | MBC3+RAM+BATTERY | Non-Japan | 0x00 | 0x03 | OK | `ea9bcae617fdf159b045185467ae58b2e4a48b9a` |
| EN implementation reference | `Pokemon - Yellow Version (USA, Europe).gbc` | 1024 KiB | 0 | MBC5+RAM+BATTERY | Non-Japan | 0x80 | 0x03 | OK | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` |

## Revision / family observations

- All 12 ROMs match their header-declared ROM size and pass both the Game Boy header checksum and global checksum.
- Japanese Red, Green, and Blue are 512 KiB. Japanese Pikachu and English Red/Blue/Yellow are 1 MiB.
- Japanese Red/Green/Blue use MBC1+RAM+BATTERY; Japanese Pikachu and English Red/Blue use MBC3+RAM+BATTERY; English Yellow uses MBC5+RAM+BATTERY.
- English Yellow sets CGB flag `0x80` (CGB-compatible). The other 11 ROMs have CGB flag `0x00`.
- All 12 set SGB flag `0x03`.
- Japanese Pikachu revisions map cleanly to header version bytes: Rev 0A=0, Rev B=1, Rev C=2, Rev D=3.
- Red/Green base revisions use header version 0; their Rev A files use header version 1. Japanese Blue is version 0 in the uploaded set.

## Consecutive revision byte differences

| Comparison | Differing bytes | Changed 16 KiB banks | Exact 16 KiB banks |
|---|---:|---:|---:|
| Aka v0 → Rev A | 46,167 | 31 | 1 |
| Midori v0 → Rev A | 46,168 | 31 | 1 |
| Pikachu 0A → B | 307,668 | 61 | 3 |
| Pikachu B → C | 39,485 | 60 | 4 |
| Pikachu C → D | 245,538 | 61 | 3 |
| English Red → Blue | 26,670 | 14 | 50 |

The revision differences are distributed across many banks, so they should not be treated as a single small patch. Future analysis should compare bank layout, pointers, text, graphics, and code separately.

## Recommended project roles

- **Primary Japanese work bases:** Red Rev A, Green Rev A, Blue v0, Pikachu Rev D.
- **Japanese revision references:** Red v0, Green v0, Pikachu Rev 0A/B/C. Keep these for revision-diff and bug-fix provenance.
- **English technical references:** Pokémon Red Version, Blue Version, Yellow Version. Use their font/encoding/text engine/UI/layout/pointer/banking implementation as technical references, not as translation originals.

## Next structural pass

1. Bank-by-bank entropy/fill/free-space map for all 12 ROMs.
2. Japanese target vs English reference bank correspondence.
3. Text engine, font/character set, string terminators, line-break commands, pointer tables, and text banks.
4. Menu/battle/status/PC/shop/Pokédex/naming UI layout differences.
5. Revision-specific code/data/text diffs, with version differences preserved.
6. Safe relocation/expansion map before any translated text insertion.
