# Pokémon LeafGreen ROM Census

- ROM count: **7**
- Size: **16 MiB (0x1000000)** each
- Source ROM binaries are intentionally **not** included in GitHub; only metadata and analysis artifacts are tracked.

## GBA Header / Identity

| File | Game code | Language/region | Rev | Header checksum | SHA-256 | Save signature |
|---|---|---|---:|---|---|---|
| Pocket Monsters - Leaf Green (Japan).gba | `BPGJ` | Japanese | 0 | OK (`7C`) | `2957b392dc09fc8df45a660af5493368d7bd378d299862f4cc115998e9da0bf2` | FLASH1M_V103@0x6C0998 |
| Pokemon - Blattgruene Edition (Germany).gba | `BPGD` | German | 0 | OK (`82`) | `6ab7183caf8bf093f42351cf7c891722ecef85f2ded922f6d2491c6062fa3fc2` | FLASH1M_V103@0x6F96A4 |
| Pokemon - Edicion Verde Hoja (Spain).gba | `BPGS` | Spanish | 0 | OK (`73`) | `f8908e0bd32cf27077a26b557e1eea0ff06ce8059bee5dc7d799aab44a070d48` | FLASH1M_V103@0x6F1F08 |
| Pokemon - Leaf Green Version (Europe) (Rev 1).gba | `BPGE` | English (source: Europe Rev 1) | 1 | OK (`80`) | `2f978f635b9593f6ca26ec42481c53a6b39f6cddd894ad5c062c1419fac58825` | FLASH1M_V103@0x6FB860 |
| Pokemon - Leaf Green Version (USA).gba | `BPGE` | English (source: USA) | 0 | OK (`81`) | `78d310d557ceebc593bd393acc52d1b19a8f023fec40bc200e6063880d8531fc` | FLASH1M_V103@0x6FB7F0 |
| Pokemon - Version Vert Feuille (France).gba | `BPGF` | French | 0 | OK (`80`) | `cc0fa93f4631d0814afcd5a273edf28f2876e126e8ef0df4dd39dd6f36e53ed3` | FLASH1M_V103@0x6F0D04 |
| Pokemon - Versione Verde Foglia (Italy).gba | `BPGI` | Italian | 0 | OK (`7D`) | `c71599a482c43df2104ce6be903393333d3ebacbf392ea5fcd8792dada8a5076` | FLASH1M_V103@0x6EF100 |

## Header facts

- All seven images are 16 MiB GBA ROMs.
- Nintendo fixed byte at `0xB2` is `0x96` for every image.
- All calculated GBA header checksums match the stored checksum.
- Software-version byte (`0xBC`) distinguishes revision level; Europe Rev 1 reports revision 1 while the other six report revision 0.

## Terminal padding candidates

The international builds end with a contiguous `0xFF` run beginning around `0xEB0E14`–`0xEB244C` (about 1.30 MiB). The Japanese build only has a final `0x20001`-byte `0xFF` run beginning at `0xFDFFFF`. These are **padding candidates only**; they are not declared safe free space until pointer/reference scans are complete.

## Pairwise binary difference summary

| A | B | Differing bytes | % of ROM | Identical 64 KiB blocks |
|---|---|---:|---:|---:|
| Pokemon - Leaf Green Version (Europe) (Rev 1).gba | Pokemon - Leaf Green Version (USA).gba | 6,424,014 | 38.290% | 142/256 |
| Pokemon - Edicion Verde Hoja (Spain).gba | Pokemon - Version Vert Feuille (France).gba | 6,688,889 | 39.869% | 137/256 |
| Pokemon - Edicion Verde Hoja (Spain).gba | Pokemon - Leaf Green Version (USA).gba | 6,995,053 | 41.694% | 137/256 |
| Pokemon - Edicion Verde Hoja (Spain).gba | Pokemon - Leaf Green Version (Europe) (Rev 1).gba | 7,011,290 | 41.791% | 137/256 |
| Pokemon - Leaf Green Version (Europe) (Rev 1).gba | Pokemon - Version Vert Feuille (France).gba | 7,015,698 | 41.817% | 137/256 |
| Pokemon - Leaf Green Version (USA).gba | Pokemon - Version Vert Feuille (France).gba | 7,018,388 | 41.833% | 137/256 |
| Pokemon - Blattgruene Edition (Germany).gba | Pokemon - Versione Verde Foglia (Italy).gba | 7,620,733 | 45.423% | 115/256 |
| Pokemon - Blattgruene Edition (Germany).gba | Pokemon - Leaf Green Version (USA).gba | 7,808,533 | 46.542% | 115/256 |
| Pokemon - Edicion Verde Hoja (Spain).gba | Pokemon - Versione Verde Foglia (Italy).gba | 7,832,045 | 46.683% | 115/256 |
| Pokemon - Blattgruene Edition (Germany).gba | Pokemon - Leaf Green Version (Europe) (Rev 1).gba | 7,848,662 | 46.782% | 115/256 |
| Pokemon - Version Vert Feuille (France).gba | Pokemon - Versione Verde Foglia (Italy).gba | 7,918,060 | 47.195% | 116/256 |
| Pokemon - Leaf Green Version (USA).gba | Pokemon - Versione Verde Foglia (Italy).gba | 8,048,315 | 47.972% | 115/256 |
| Pokemon - Leaf Green Version (Europe) (Rev 1).gba | Pokemon - Versione Verde Foglia (Italy).gba | 8,057,172 | 48.024% | 115/256 |
| Pokemon - Blattgruene Edition (Germany).gba | Pokemon - Version Vert Feuille (France).gba | 8,072,766 | 48.117% | 115/256 |
| Pokemon - Blattgruene Edition (Germany).gba | Pokemon - Edicion Verde Hoja (Spain).gba | 8,093,415 | 48.241% | 115/256 |
| Pocket Monsters - Leaf Green (Japan).gba | Pokemon - Versione Verde Foglia (Italy).gba | 10,418,854 | 62.101% | 85/256 |
| Pocket Monsters - Leaf Green (Japan).gba | Pokemon - Version Vert Feuille (France).gba | 10,418,986 | 62.102% | 85/256 |
| Pocket Monsters - Leaf Green (Japan).gba | Pokemon - Edicion Verde Hoja (Spain).gba | 10,425,312 | 62.140% | 84/256 |
| Pocket Monsters - Leaf Green (Japan).gba | Pokemon - Leaf Green Version (USA).gba | 10,470,545 | 62.409% | 84/256 |
| Pocket Monsters - Leaf Green (Japan).gba | Pokemon - Blattgruene Edition (Germany).gba | 10,476,307 | 62.444% | 84/256 |
| Pocket Monsters - Leaf Green (Japan).gba | Pokemon - Leaf Green Version (Europe) (Rev 1).gba | 10,477,060 | 62.448% | 84/256 |

## Next census stages

1. Bank/section map and executable/data segmentation.
2. Text encoding, fonts, string tables, and pointer families per language.
3. Graphics/tile/palette/audio/resource inventories.
4. Map/event/NPC/trainer/wild/item/script tables and version deltas.
5. Cross-language correspondence ledger and revision-specific diffs.
6. Free-space/unused/test/debug data census.
7. Reproducible extraction scripts and regression checks.
