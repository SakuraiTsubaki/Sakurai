# Generation IV battle sprites -> Generation III integration v1

## Goal

Preserve the existing DP / Platinum / HGSS 64x64 battle-sprite masters and make every logical sprite variant addressable from Generation III without deleting or overwriting the original Generation III assets.

## Confirmed Generation IV source masters in Tsubaki

- Diamond / Pearl: 493 base National Dex species, 7,768 logical PNG records, including corrected alternate forms.
- Platinum: 493 base National Dex species, 7,840 logical PNG records.
- HeartGold / SoulSilver: 493 base National Dex species, 7,864 logical PNG records.
- Combined master documentation: 25,136 logical records and 11,947 SHA-256-unique 64x64 rendered assets after cross-title deduplication.

All masters retain source-game differences, gender-specific front/back graphics where present, normal/shiny rendering, alternate forms, and all published animation frames. DP alternate forms use the corrected reverse LCRNG-XOR NCGR decryption path already recorded in the Generation IV project.

## Uploaded Japanese Generation III ROM baselines

Read-only originals currently available to the project workspace:

| Game | Header code | Revision | Original size |
| --- | --- | ---: | ---: |
| Pocket Monsters Ruby | AXVJ | 0 | 8 MiB |
| Pocket Monsters Sapphire | AXPJ | 0 | 8 MiB |
| Pocket Monsters Emerald | BPEJ | 0 | 16 MiB |
| Pocket Monsters FireRed | BPRJ | 1 | 16 MiB |
| Pocket Monsters LeafGreen | BPGJ | 0 | 16 MiB |

The originals stay read-only. Work copies / patches are separate.

## Asset conversion contract

`build_gen4_battle_pack.py` converts every Tsubaki 64x64 logical PNG to:

- GBA OBJ 4bpp tiled graphics (2048 bytes uncompressed per frame)
- one 16-color little-endian BGR555 palette, palette slot 0 transparent
- independently GBA BIOS-LZ77 type-0x10 compressed graphics
- 4-byte-aligned concatenated graphics pack
- deduplicated palette pack
- logical -> graphics/palette ID index retaining DP / Pt / HGSS provenance

No antialiasing, interpolated colors, AI generation, nearest-title collapse, or destructive replacement is introduced by this stage.

## Engine integration strategy

Generation III already separates front graphics, back graphics, normal palettes, shiny palettes, and front/back coordinate tables. RSE and FRLG therefore receive an expanded pointer/table layer rather than replacing the original tables.

1. Keep the original Gen III front/back/palette data addressable.
2. Add the Gen IV graphics/palette pack in expanded ROM space.
3. Create extended logical sprite metadata keyed by species/form/gender/source-title/side/palette/frame.
4. Use frame 0 as the static compatibility frame for existing Gen III draw paths.
5. Add an extended animation path for additional Gen IV frames instead of discarding them.
6. Expand species/form lookup independently from the graphics storage so 001-386 originals and 387-493/new forms can coexist.
7. Validate battle, summary/status, Pokédex, evolution, contest/PokéNav-style consumers, egg/hatch, and any routines that directly index the original graphics tables.

## Repository split

- `Sakurai`: analysis, source code, mapping, validation, reports.
- `Tsubaki`: generated reusable game assets and build resources.
- ROM binaries are never committed.
