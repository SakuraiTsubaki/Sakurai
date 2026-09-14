# Pokémon White IRAO-HV0 — direct ROM structural audit (Phase W1)

## Source

- Observed filename: `Pokemon.White.Version.EUR.NDS-SweeTnDs.nds`
- Size: **268,435,456 bytes**
- MD5: `8dfef9a099e1269af5c1fcf9d7736a11`
- SHA-1: `f94d4578956487c09fee20809a591e858017769e`
- SHA-256: `93e4f473ce9a0543bccf2e689ecd07ab4fcc39dd00fb4f194343cbd5e70e17ed`
- ROM binary committed: **no**

## Header identity

- Internal title: `POKEMON W`
- Game code: `IRAO`
- Maker code: `01`
- Unit code: `0x02`
- Header ROM version: `0`
- Device capacity code: `11` → 268,435,456 bytes
- Header logical ROM size: 205,231,104 bytes
- Header size: 16,384 bytes

## Executable / filesystem layout

- ARM9: ROM `0x00004000`, load `0x02004000`, entry `0x02004800`, size 456,868
- ARM7: ROM `0x002C7E00`, load `0x02380000`, entry `0x02380000`, size 167,812
- FNT: `0x002F0E00` + 1,040
- FAT: `0x002F1400` + 3,872
- ARM9 overlay table: `0x00073A00` + 7,584 = **237 records**
- ARM7 overlay table: **0 records**
- NitroFS FAT entries: **484**
- FNT directories: **31**
- Named NitroFS files: **247**
- Overlay-owned unnamed FAT files: **237**
- NARC containers: **237**
- NARC member files total: **54,054**
- Last FAT allocation ends at `0x0BFD9C3C` (201,169,980)

The 237 unnamed FAT entries map one-for-one to the 237 ARM9 overlay records. The remaining 247 named files are the named NitroFS payload. Of those named files, 237 are NARC archives; the remaining ten are font/audio/download-play/DWC support files.

## Confirmed/high-confidence core archives

| Path | Members | Member-size range | Role | Status |
|---|---:|---:|---|---|
| `a/0/0/2` | 288 | 20..252092 | system_message_text | confirmed |
| `a/0/0/3` | 472 | 32..160444 | story_field_text | confirmed |
| `a/0/1/2` | 1 | 20496..20496 | zone_data_map_association | confirmed |
| `a/0/1/6` | 669 | 56..1300 | pokemon_personal_parameters | confirmed |
| `a/0/1/7` | 8 | 404..404 | experience_growth_tables | confirmed |
| `a/0/1/8` | 668 | 4..92 | level_up_learnsets | confirmed |
| `a/0/1/9` | 668 | 42..42 | evolution_data | confirmed |
| `a/0/2/0` | 650 | 2..2 | baby_base_species_table | confirmed |
| `a/0/2/1` | 560 | 36..36 | move_parameters | confirmed |
| `a/0/2/4` | 627 | 36..36 | item_parameters | high |
| `a/0/2/6` | 15 | 114..14173 | title_version_assets | confirmed |
| `a/0/5/7` | 899 | 4..33176 | field_map_scripts | high |
| `a/0/9/2` | 616 | 16..20 | trainer_data_trdata | confirmed |
| `a/0/9/3` | 616 | 6..108 | trainer_party_trpoke | confirmed |
| `a/1/2/3` | 650 | 0..34 | egg_move_data | high |
| `a/1/2/5` | 428 | 4..2178 | overworld_event_objects | confirmed |
| `a/1/2/6` | 112 | 232..928 | wild_encounter_data | confirmed |
| `a/1/7/8` | 649 | 249..249 | pokedex_availability_location_matrix_candidate | high_inferred |

## High-value observations for the White-first pass

1. `a/0/1/2` is a single-member NARC whose payload is the zone-data association table. This is the structural spine for joining maps to scripts and overworld objects.
2. `a/0/1/6`, `a/0/1/8`, `a/0/1/9`, `a/0/2/1`, `a/0/2/4`, `a/0/9/2`, `a/0/9/3`, `a/1/2/6` are the first record-level decode targets for Pokémon, learnsets/evolution, moves, items, trainers and encounters.
3. `a/0/2/6` is retained as version/title assets; White-specific deltas will be recorded under the White release first and only later mirrored into a cross-version comparison.
4. `a/1/7/8` remains explicitly **high_inferred**, not promoted to confirmed until its 649×249-byte semantic fields are decoded and runtime references are traced.
5. No extracted copyrighted ROM binary payload is stored by this phase; only metadata, hashes, structure tables and tooling are intended for GitHub.

## Next White-only phases

- **W2:** decode Pokémon personal records, growth curves, learnsets, evolution, moves and item records.
- **W3:** decode trainer metadata/party structures and wild encounter tables.
- **W4:** decode ZoneData → scripts → overworld linkage and reconstruct the White map/event graph.
- **W5:** locate White-specific executable/overlay logic and distinguish code relocation/compression differences from gameplay deltas.
- **W6:** text container decoding, message index map, glyph/font linkage and English-localization structure.
- **W7:** graphics/audio resource classification, unused/dummy reachability tracing, then preservation/normalization planning.

## Provenance / confidence

All counts, offsets, hashes and archive-size observations in this report were recomputed directly from the supplied White ROM. Semantic labels are carried only where prior BW-specific research is strong enough to support them and retain an explicit confidence state.
