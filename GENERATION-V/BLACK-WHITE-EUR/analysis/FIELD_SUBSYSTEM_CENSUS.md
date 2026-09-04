# Pokémon Black/White EUR — Field subsystem census

No ROM bytes were modified. This phase links BW1 ZoneData to the script, overworld/event-object and encounter archives using values read directly from the Black ROM.

## 1. Verified archive linkage

- `a/0/1/2`: ZoneData, one member of **20,496 B = 427 × 48 B**.
- `a/0/5/7`: field/event archive, **899 members**.
- `a/1/2/5`: overworld/NPC/map-event object data, **428 members**.
- `a/1/2/6`: wild encounters, **112 members**.

For every ZoneData record `i = 0..426` with **no exceptions**:

- `+0x06` = **2 × i** → executable Script Set A member.
- `+0x08` = **2 × i + 1** → Script Set B metadata member.
- `+0x14` = encounter member **0..111**, or `0xFFFF`. Across all rows the non-FFFF set is exactly **0..111**.
- `+0x16` = **i** → overworld member.

Regular ZoneData therefore covers script members **0..853**, overworld members **0..426**, and all 112 encounter members. `a/0/5/7` has **45 extra members 854..898** and `a/1/2/5` has one extra member **427**.

## 2. Script A / Script B split — locally proven

The 899-member `a/0/5/7` archive has a previously under-documented alternating layout for the regular 427 zones:

- **all 427 even members** (`0,2,...,852`) contain a valid BW declarative script header: UInt32 relative offsets followed on disk by `13 FD`; all computed script targets are in-range. These 427 files declare **2,064 scripts** in total, max **33** in one zone member.
- **all 427 odd members** (`1,3,...,853`) contain no such executable-script header.
- of the **45 extra members** (`854..898`), **43** contain valid executable script headers, declaring another **525 scripts**; members **863 and 865** do not match the normal script header format and remain data-table/custom members.

So the archive contains at least **2,589 declared executable script entry points** in locally validated headers.

## 3. Exact duplicate discovered: Script Set B == overworld tail

Every regular overworld member was parsed as:

`8-byte header + furniture(0x14 each) + NPC(0x24 each) + warp(0x14 each) + trigger(0x16 each) + tail`

For **all 427 zones**, the resulting `tail` is **byte-for-byte identical** to `a/0/5/7` member `2*i+1` — the exact Script Set B file selected by ZoneData `+0x08`. There are **427/427 exact matches**.

The first u32 of each overworld member also satisfies, for all 427 members:

`read_length = main_structure_end - 4`

The extra overworld member **427** is only `00 00 00 00`, confirming it is outside the normal 427 ZoneData mapping.

Across the 427 normal overworlds the locally parsed object totals are:

- furniture: **662**
- NPC/interactable records: **2,257**
- warps: **886**
- floor triggers: **373**

Historical BW research describes the overworld tail as extra/global-script trigger metadata. The local byte-identity proof now ties that metadata directly to ZoneData's Script Set B member rather than treating it as unrelated padding.

## 4. ZoneData record 158 cross-check

```text
00 10 16 00 67 00 3c 01 3d 01 a6 00 36 04 36 04 36 04 36 04 08 00 9e 00 9d 00 22 04 00 00 40 6d 67 00 00 00 05 00 00 00 00 00 00 00 04 00 00 00
```

This gives Script Set A `0x013C=316`, Set B `0x013D=317`, encounter `8`, and overworld `158`. The `316/317` pairing is exactly `2×158 / 2×158+1`. Historical BW research independently uses this same 48-byte record as the Desert Resort example.

## 5. ZoneData semantic field ledger

Strong local proof exists for offsets `0x06`, `0x08`, `0x14`, `0x16`, and the always-zero fields. Historical BW research additionally catalogs `0x0A` as the text-bank selector, `0x18` as the current-location/submap field, camera/field flags at `0x1C..0x20`, and FlyTo coordinates at `0x24/0x28/0x2C`. Less certain historical labels remain explicitly marked tentative; no guessed name is promoted to confirmed.

## 6. Generated ledgers

- `field_zonedata_links.csv`: concise 427-row ZoneData→script/encounter/overworld map.
- `field_zonedata_full.csv`: all 24 u16 fields for all 427 ZoneData rows.
- `field_zonedata_column_stats.csv`: value-domain census per ZoneData column.
- `field_zonedata_semantic_fields.csv`: semantic/confidence ledger for all 24 u16 fields.
- `field_script_archive_census.csv`: all 899 field archive members, sizes, pairing role, executable-header status, declared script counts, hashes.
- `field_overworld_layout_census.csv`: all 428 overworld members with object counts, section lengths, tail sizes, and tail↔odd-member equality.
- `field_subsystem_summary.json`: machine-readable verification summary.
