# Generation IV ROM Analysis — 2026-09-04

## Scope

Five Nintendo DS ROM images were inspected directly at the binary level. No ROM bytes are included in this report.

- Pokémon Diamond (USA, English)
- Pokémon Pearl (USA, English)
- Pokémon Platinum / 포켓몬스터Pt 기라티나 (Korea)
- Pokémon HeartGold / 포켓몬스터 하트골드 (Korea)
- Pokémon SoulSilver / 포켓몬스터 소울실버 (Korea)

The analysis parses the NDS header, ARM9/ARM7 regions, overlay tables, FNT/FAT NitroFS, and NARC archive headers/entry tables. Selected NARCs were compared entry-by-entry.

## ROM identity

| ROM | Game code | Size | Header version byte | SHA-1 |
|---|---:|---:|---:|---|
| Diamond USA | ADAE | 64 MiB | 5 | `a46233d8b79a69ea87aa295a0efad5237d02841e` |
| Pearl USA | APAE | 64 MiB | 5 | `99083bf15ec7c6b81b4ba241ee10abd9e80999ac` |
| Platinum KR | CPUK | 128 MiB | 0 | `f811d9c7ab5262f593012da794c2fa81dbcdbcc1` |
| HeartGold KR | IPKK | 128 MiB | 0 | `5834fb3a2d751c48501d47d6a56898d7af6ccf9e` |
| SoulSilver KR | IPGK | 128 MiB | 0 | `0330e6449306606114a92bdbb3f9d3d51d392b96` |

The Diamond/Pearl SHA-1 values exactly match the reference baseroms used by `pret/pokediamond`, and external version databases identify those hashes as USA Rev 5.

## NDS structural summary

| ROM | ARM9 size | ARM7 size | FAT entries | Named NitroFS files | Directories | ARM9 overlays | NARC archives |
|---|---:|---:|---:|---:|---:|---:|---:|
| Diamond | 1,079,076 | 168,732 | 356 | 269 | 69 | 87 | 149 |
| Pearl | 1,079,076 | 168,732 | 356 | 269 | 70 | 87 | 149 |
| Platinum KR | 1,061,624 | 161,788 | 461 | 339 | 105 | 122 | 215 |
| HeartGold KR | 765,204 | 161,496 | 511 | 382 | 46 | 129 | 308 |
| SoulSilver KR | 765,208 | 161,496 | 511 | 382 | 46 | 129 | 308 |

### Filesystem style

- Diamond/Pearl retain descriptive NitroFS paths such as `poketool/personal/personal.narc`, `msgdata/msg.narc`, and `fielddata/script/scr_seq_release.narc`.
- Platinum retains the same descriptive layout but frequently stores base D/P data alongside active Platinum replacements prefixed with `pl_`.
- HeartGold/SoulSilver strip many core archive names into serial paths such as `a/0/0/2`, `a/0/2/7`, etc. The mappings match the `pret/pokeheartgold` filesystem definitions.

## Core data archive counts

| Data | Diamond/Pearl | Platinum active | HeartGold/SoulSilver |
|---|---:|---:|---:|
| Personal data | 501 | 508 (`pl_personal`) | 508 (`a/0/0/2`) |
| Evolutions | 501 | 508 | 508 (`a/0/3/4`) |
| Learnsets | 501 | 508 | 508 (`a/0/3/3`) |
| Move table | 471 | 471 | 471 (`a/0/1/1`) |
| Pokémon battle sprite archive | 2,964 | 2,964 | 2,964 (`a/0/0/4`) |
| Pokémon icon archive | 540 | 547 | 551 (`a/0/2/0`) |
| Main message archive | 624 | 714 (`pl_msg`) | 822 (`a/0/2/7`) |
| Field scripts | 1,051 | 1,124 | 965 (`a/0/1/2`) |
| Map matrices | 245 | 289 | 288 (`a/0/4/1`) |
| Trainer data | 850 | 928 | 738 (`a/0/5/5`) |
| Trainer parties | 850 | 928 | 738 (`a/0/5/6`) |

The 508-slot personal/evolution/learnset layout in Platinum and HGSS corresponds to the Gen IV expanded internal species/form space. The public HGSS constants identify slots through Rotom's appliance forms up to internal species index 507.

## Diamond vs Pearl — exact version delta

At the named NitroFS level, Diamond and Pearl are almost completely identical:

- 268 common named files are byte-identical.
- Diamond has `poketool/personal/personal.narc`.
- Pearl has `poketool/personal_pearl/personal.narc`.
- Those two personal archives contain 501 entries each and differ at only six species indexes:
  - 125 Electabuzz
  - 126 Magmar
  - 239 Elekid
  - 240 Magby
  - 466 Electivire
  - 467 Magmortar

All six differences are confined to bytes 12–15 of the 44-byte personal record. These are the two held-item fields. The values `0x0142` and `0x0143` swap between the two held-item slots, matching Electirizer/Magmarizer version-specific held-item behavior.

Binary/code differences also exist outside named NitroFS:

- ARM7 is byte-identical.
- ARM9 differs.
- 18 of 87 ARM9 overlay payloads differ.
- Therefore the version identity is not represented only by the personal archive; code/overlay build differences also participate.

## Platinum — D/P base data plus active `pl_` replacements

Platinum KR keeps many D/P-era archives while adding active Platinum versions. Examples:

- `msgdata/msg.narc` — 612 entries
- `msgdata/pl_msg.narc` — 714 entries
- `poketool/personal/personal.narc` — 501 entries
- `poketool/personal/pl_personal.narc` — 508 entries
- `poketool/pokegra/pokegra.narc` — 2,964 entries
- `poketool/pokegra/pl_pokegra.narc` — 2,964 entries
- `itemtool/itemdata/item_data.narc` — 442 entries
- `itemtool/itemdata/pl_item_data.narc` — 446 entries

The D/P Diamond personal archive is byte-identical to Platinum's preserved 501-entry base `personal.narc`.

### Platinum expansion indicators

Compared with D/P:

- ARM9 overlays: 87 → 122
- FAT entries: 356 → 461
- NARC archives: 149 → 215
- Main active text: 624 → 714 entries
- Field scripts: 1,051 → 1,124
- Map matrices: 245 → 289
- Trainers: 850 → 928
- Personal/evolution/learnset slots: 501 → 508

## HeartGold/SoulSilver serial archive map

Confirmed examples:

| HGSS path | Meaning |
|---|---|
| `a/0/0/2` | Pokémon personal data |
| `a/0/0/3` | growth tables |
| `a/0/0/4` | Pokémon battle graphics (`pokegra`) |
| `a/0/1/1` | move table |
| `a/0/1/2` | field scripts |
| `a/0/1/6` | font archive |
| `a/0/1/7` | item data |
| `a/0/1/8` | item icons |
| `a/0/2/0` | Pokémon icons |
| `a/0/2/7` | main message archive |
| `a/0/3/3` | learnsets |
| `a/0/3/4` | evolutions |
| `a/0/3/7` | Gold encounter table |
| `a/1/3/6` | Silver encounter table |
| `a/0/5/5` | trainer data |
| `a/0/5/6` | trainer parties |
| `a/1/4/1` | follower Pokémon parameters |
| `a/2/6/2` | opening graphics/data |

This mapping is corroborated by the current `pret/pokeheartgold` filesystem build definitions.

## HeartGold vs SoulSilver — exact named filesystem delta

The two Korean ROMs contain the same 382 named NitroFS paths.

- 379 named files are byte-identical.
- Only three named files differ:
  - `a/0/7/5` — version-specific Pokédex height/weight data
  - `a/1/3/3` — version-specific Pokédex encounter data
  - `a/2/5/2` — version-specific Headbutt encounter archive

The core Gold and Silver encounter NARCs are both physically present in both ROMs (`a/0/3/7` and `a/1/3/6`), so runtime/build logic selects the relevant version data rather than each ROM containing only one encounter set.

ARM7 is byte-identical. ARM9 and a large number of overlay payloads differ between the two builds, so the HG/SS version split is strongly represented in executable code as well.

## Sprite lineage — direct entry-by-entry evidence

The principal battle sprite archive has 2,964 members in D/P, Platinum, and HGSS. This is exactly 494 × 6, i.e. six archive members per base species slot from index 0 through 493.

### D/P → Platinum active sprites

Comparing Diamond `pokegra.narc` against Platinum `pl_pokegra.narc`:

- 1,996 of 2,964 archive members differ.
- All 494 species groups have at least one changed member.

Platinum therefore represents a broad generation-wide sprite refresh, not a small patch set.

### Platinum → HGSS sprites

Comparing Platinum `pl_pokegra.narc` against HGSS `a/0/0/4`:

- 751 of 2,964 archive members differ.
- 264 species groups contain at least one changed member.
- Most differences are concentrated in species 1–251, with a small number of later-species changes.

This directly supports the asset priority:

1. HGSS
2. Platinum
3. Diamond/Pearl fallback

### Other sprite/icon expansions

- Platinum `pl_otherpoke.narc`: 253 entries
- HGSS `otherpoke`: 261 entries, with 8 additional entries
- Platinum `pl_poke_icon.narc`: 547 entries
- HGSS Pokémon icons: 551 entries; the first 547 entries are byte-identical and HGSS appends 4 entries

## Move-table continuity

Platinum active and HGSS move tables both contain 471 entries. They are byte-identical except for move index 258 (Hail), where one byte at record offset 11 changes from `0x02` in Platinum to `0x00` in HGSS.

This is a useful marker for distinguishing otherwise nearly identical Gen IV move-table formats.

## Korean text/font architecture

### Font archives

| Build | Font NARC | Entries | Approx. archive size |
|---|---|---:|---:|
| Diamond EN | `graphic/font.narc` | 8 | 134,744 bytes |
| Platinum KR base | `graphic/font.narc` | 10 | 759,840 bytes |
| Platinum KR active | `graphic/pl_font.narc` | 10 | 759,912 bytes |
| HGSS KR | `a/0/1/6` | 13 | 1,201,508 bytes |

The Korean builds therefore use substantially expanded font resources rather than merely swapping a small character table.

All five ROMs also contain the exact same `data/nfont.NCGR` and `data/nfont.NCLR` system graphic pair (matching SHA-1 across all five), so that small shared font resource is not the main language font archive.

### Platinum Korean localized resource tree

Platinum KR exposes a large `resource/kor/` tree containing localized UI/graphic archives for battle lists, bag, battle recording, battle graphics, boxes, contests, dress-up, Battle Frontier, name input, opening demo, status screen, Pokétch, slots, title demo, trainer card/case, Pokédex, VS demo, Wi-Fi lobby minigames, and more.

HGSS no longer exposes a comparable readable `resource/kor/` directory; many equivalent assets are serialized into the `a/X/Y/Z` namespace.

## Modification implications

For future extraction/replacement work:

1. Treat each ROM as a full NDS filesystem with ARM9 + overlays + NitroFS, not as a flat data blob.
2. Prefer NARC-level replacement where the target archive is known.
3. For HGSS, always resolve stripped `a/X/Y/Z` paths to semantic names before editing.
4. Preserve archive member count/order unless engine code is deliberately expanded.
5. For Pokémon data, use 508-slot Pt/HGSS structures when working with Gen IV form data.
6. For sprite sourcing, use HGSS first, then Platinum, then D/P only where no later Gen IV asset exists.
7. Keep Korean font/text assets separate from the small shared `nfont` system graphic.
8. Do not assume HeartGold and SoulSilver differ only in encounters: executable overlays are separately built and many differ at binary level.

## External structural references

- `pret/pokediamond` — decompilation builds the exact Diamond/Pearl USA SHA-1 baseroms used here.
- `pret/pokeheartgold/filesystem.mk` — maps stripped HGSS `a/X/Y/Z` archives back to semantic filenames.
- `pret/pokeheartgold/include/constants/species.h` — documents the 508-entry Gen IV internal species/form index space used by HGSS.
