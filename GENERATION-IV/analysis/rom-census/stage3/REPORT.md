# Generation IV ROM Census — Stage 3

## Scope

Stage 3 extends the five-ROM census into the text/glyph, script-entry, event-record, sprite-slot, residual-asset, and HGSS executable-difference layers. ROM bytes are not included in repository artifacts.

## Korean character system and message rendering

The Generation IV message stream is a 16-bit character/control stream. The Korean mapping used here was reconstructed from the shared Generation IV charset, including the KS X 1001 Hangul block and the Korean extension area. The local mapping contains 2,873 mapped visible/symbol codepoints, including 2,350 KS X 1001 Hangul syllables, 33 Hangul jamo, and the five extra syllables `뢔 쌰 쎼 쓔 쬬`.

The active HGSS archive contains **47,515 messages in 822 banks**. After MAT decryption and control-code parsing, visible code-unit mapping coverage is **100.000000%** (1,148,362/1,148,362); 0 visible code units remain unmapped in the conservative table. No `0xF100` compressed-message marker occurs in the active HGSS archive.

Direct sanity checks from the Korean ROM decode:

- message bank 233, entry 1: `이상해씨`
- message bank 743, entry 1: `막치기`
- message bank 743, entry 53: `화염방사`
- message bank 743, entry 57: `파도타기`
- message bank 743, entry 98: `전광석화`

The complete 47,515-row rendered-message ledger is kept in the local Stage 3 package and is deliberately **not** committed to the public repository. The repository keeps hashes, counts, summaries, and the reproducible builder instead.

## Font/glyph structure

The font member header is parsed as `headerSize`, `widthDataStart`, `numGlyphs`, fixed width/height, and tile width/height. HGSS main font archive `a/0/1/6` contains large font members with **3,440 glyphs**, enough to address the Korean extension through character code `0x0D65` (3429). This agrees with the runtime behavior that uses character/glyph IDs almost directly (`glyphId - 1`).

## Battle sprite slots and alternate forms

The main battle Pokémon graphics archive in every target still resolves to **494 six-member groups**. Stage 3 maps the ordinary groups as slot 0 = none and slots **1–493 = National species IDs 1–493**. Alternate-form graphics are stored in separate `otherpoke`/`pl_otherpoke`-lineage archives; HGSS uses `a/1/1/4` for its current alternate-form archive and also retains the older `pbr/otherpoke.narc`.

HeartGold and SoulSilver main battle-sprite archives are byte-identical: **True**. Their current alternate-form archive is also byte-identical: **True**.

## Script-entry census

Field bytecode dispatch reads a 16-bit opcode and validates it against the script command table. Current HGSS decompilation exposes **853 command slots (0–852)**. Stage 3 parses every script bank's entry-pointer table (32-bit relative offsets terminated by `0xFD13`) and validates each entry's initial opcode.

| ROM | NARC members | Bytecode banks | Script-header banks | Unresolved | Entry points |
|---|---:|---:|---:|---:|---:|
| Diamond_USA | 1,051 | 535 | 512 | 4 | 3,399 |
| Pearl_USA | 1,051 | 535 | 512 | 4 | 3,399 |
| Platinum_KOR | 1,124 | 572 | 549 | 3 | 4,059 |
| HeartGold_KOR | 965 | 497 | 468 | 0 | 3,893 |
| SoulSilver_KOR | 965 | 497 | 468 | 0 | 3,893 |

The NARC intentionally mixes executable script banks with map-script-header banks. Stage 3 classifies both forms separately, records every validated bytecode entry and relative pointer target, and parses the 5-byte map-script-header records plus scene-condition tables. It does not falsely treat arbitrary header/argument halfwords as opcodes.

## HGSS event-record census

HGSS zone-event members were decoded in their on-ROM order: background events, object/NPC events, warps, then coordinate events. The object records expose sprite ID, movement, event flag, script ID, facing, parameters, ranges and coordinates.

| ROM | Event banks | Valid banks | BG events | Object/NPC events | Warps | Coordinate events |
|---|---:|---:|---:|---:|---:|---:|
| HeartGold_KOR | 491 | 491 | 1,034 | 2,667 | 1,317 | 195 |
| SoulSilver_KOR | 491 | 491 | 1,034 | 2,667 | 1,317 | 195 |

The entire HGSS event NARC is byte-identical between HeartGold and SoulSilver: **True**.

## HeartGold vs SoulSilver executable layer

The two versions share overwhelmingly identical data resources, but the executable layer carries widespread compile-time/version-specific differences. The direct binary census finds:

- ARM9 different common bytes: **712,099**
- ARM7 different common bytes: **0**
- ARM9 overlays compared: **129**
- byte-identical overlays: **11**
- different overlays: **118**

This matches the source-level model in which `GAME_VERSION` is compiled as HeartGold or SoulSilver and scripts can query the result through `GetGameVersion`; version-specific routines also branch on that value.

## Residual / compatibility assets

Stage 1 exact-hash mapping identified **146 HGSS numbered-path objects** that are exact matches for named DPPt-lineage assets. Stage 3 carries those mappings forward as a dedicated residual-asset ledger, including retained PBR/DPPt compatibility resources. This is evidence of deliberate asset reuse and compatibility layers, not by itself evidence that an asset is reachable in normal HGSS play. Reachability classification remains separate from exact-hash identity.

## Canonical Stage 3 local artifacts

- `character_map.csv`
- `hgss_messages_text.csv` — all 47,515 active Korean messages (local package only)
- `message_bank_render_summary.csv`, `message_control_usage.csv`, `message_unknown_codes.csv`
- `font_headers.csv`
- `battle_sprite_species_slots.csv`, `alternate_form_archive_census.csv`
- `script_entries.csv`, `script_bank_summary.csv`, `script_header_records.csv`, `script_first_opcode_usage.csv`
- `event_records_hgss.csv`, `event_member_summary.csv`
- `hgss_arm_overlay_diffs.csv`
- `legacy_exact_asset_mappings.csv`
- `key_findings.json`, `ARTIFACT_MANIFEST.json`
- `tools/build_stage3.py`

## Validation references

The ROM-derived counts and hashes in this report come from the five uploaded project ROMs. External reverse-engineering sources are used to validate structures and semantics, especially `pret/pokeheartgold` (`src/msgdata.c`, `src/font_data.c`, `src/script.c`, `src/data/fieldmap/script_cmd_table.h`, `src/map_events.c`, `include/map_events_internal.h`) and the published HGSS character-map work.
