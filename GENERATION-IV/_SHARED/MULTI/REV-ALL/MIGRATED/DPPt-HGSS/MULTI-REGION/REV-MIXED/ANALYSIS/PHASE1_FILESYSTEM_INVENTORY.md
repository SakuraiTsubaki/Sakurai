# Generation IV Phase 1 — NDS filesystem / executable inventory

## Scope

Source is the five user-supplied read-only Nintendo DS ROM images. ROM binaries are not redistributed. This phase inventories the NDS header executable regions, ARM9 overlay table, FNT/FAT, NitroFS paths, NARC archives/member counts, and pairwise version deltas.

## Global inventory

| Game | Code | Rev | ROM size | ARM9 size | ARM7 size | ARM9 overlays | Named NitroFS files | FAT total | NARCs | NARC members |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Diamond | `ADAE` | 5 | 67108864 | 1079076 | 168732 | 87 | 269 | 356 | 149 | 33953 |
| Pearl | `APAE` | 5 | 67108864 | 1079076 | 168732 | 87 | 269 | 356 | 149 | 33953 |
| Platinum | `CPUK` | 0 | 134217728 | 1061624 | 161788 | 122 | 339 | 461 | 215 | 53505 |
| HeartGold | `IPKK` | 0 | 134217728 | 765204 | 161496 | 129 | 382 | 511 | 308 | 56674 |
| SoulSilver | `IPGK` | 0 | 134217728 | 765208 | 161496 | 129 | 382 | 511 | 308 | 56674 |

`FAT total - named NitroFS files == ARM9 overlay count` for all five ROMs. Therefore the FAT records lacking FNT names in this inventory are the ARM9 overlay payloads, not evidence of unused files. None of the five baselines has an ARM7 overlay table.

## Executable hashes

| Game | ARM9 SHA-1 | ARM7 SHA-1 |
|---|---|---|
| Diamond | `dde6a342ad7c12f4f7362a252ca6a6dc7d93b4e7` | `39aacbf97ae65b17783057aeed06b80049b18dee` |
| Pearl | `3d3633517922c35d5e9a328f99ca73a43f310aac` | `39aacbf97ae65b17783057aeed06b80049b18dee` |
| Platinum | `350a768bf5a5dd7faf9b04dabcc7b848f8212124` | `082bb349ae7d057edbbd91a07316b1402b18b803` |
| HeartGold | `46413616c2e77d836ef09cdd01c04eaf206ee791` | `1d0b3418b85fa8b5e1a9e345d3a182073cb968ac` |
| SoulSilver | `8cf2235dc1fb9f01bcb42ba52e0f12af9d05e078` | `1d0b3418b85fa8b5e1a9e345d3a182073cb968ac` |

Diamond/Pearl share a byte-identical ARM7 but have different ARM9 images. HeartGold/SoulSilver likewise share a byte-identical ARM7 while their ARM9 images differ.

## Diamond vs Pearl

All shared named NitroFS files are byte-identical. The version-specific species personal archive is stored at `poketool/personal/personal.narc` in Diamond and `poketool/personal_pearl/personal.narc` in Pearl. Both contain 501 records and are 26104 bytes; exactly six members differ: **125, 126, 239, 240, 466, 467**.

18 of the 87 ARM9 overlays differ: **5, 6, 7, 8, 11, 12, 16, 17, 18, 48, 54, 62, 63, 64, 80, 81, 83, 84**.

## Platinum expansion relative to Diamond/Pearl

Platinum increases the FAT inventory from 356 to 461 records, ARM9 overlays from 87 to 122, NARCs from 149 to 215, and aggregate NARC members from 33953 to 53505. Its named tree adds or expands `frontier/`, `debug/`, `resource/`, `particledata/`, `application/`, `arc/`, and `poketool/` content. Platinum also carries separate Diamond, Pearl, and Platinum Pokédex encounter archives.

## HeartGold vs SoulSilver

The full FAT/path layout is identical: 511 FAT entries, 382 named files, 129 ARM9 overlays. 121 FAT records differ by content: **118 overlays + 3 named NitroFS files**.

The three named differences are:

- `a/0/7/5` — decompilation NARC ID 75, Pokédex height/weight data (`zukan_hw_data`); 1 of 2 members differs.
- `a/1/3/3` — decompilation NARC ID 133, Pokédex encounter data (`zukan_enc`); 130 of 3962 members differ.
- `a/2/5/2` — decompilation NARC ID 254, Headbutt encounter archive (`arc_headbutt`); 33 of 540 members differ.

HG/SS each contain 308 NARCs and 56674 aggregate NARC members.

## Important classification rule

HGSS contains large compatibility/legacy-looking families such as `pbr/`, D/P-era `data/` resources, Wi-Fi/DWC resources, Underground assets and Pal Park-related data. Presence or naming alone is **not** sufficient to mark any of these unused. Later phases must trace code references, scripts, table users, and runtime reachability before assigning `live`, `version-specific`, `leftover`, `unused`, `dummy`, or `reserved` status.

## Largest NARCs observed

- D/P: `fielddata/land_data/land_data_release.narc` (14778156 bytes, 578 members), `poketool/pokegra/pokegra.narc` (11778676, 2964), `msgdata/msg.narc` (2695184, 624).
- Platinum: `fielddata/land_data/land_data.narc` (16125840, 666), `poketool/pokegra/pl_pokegra.narc` and `poketool/pokegra/pokegra.narc` (11778676, 2964 each), `msgdata/pl_msg.narc` (2654348, 714).
- HG/SS: `a/0/6/5` (19536644, 676), `a/0/0/4` and `pbr/pokegra.narc` (11778676, 2964 each), `a/0/8/1` (4637368, 863).

## Phase status

**Phase 1 complete for the five supplied ROM baselines.** The container/executable/filesystem map is stable enough to begin semantic extraction.

Next phase: resolve each archive/member to concrete game structures — species, forms, moves, items, evolutions, encounters, trainers, scripts, maps, text, graphics and sound — then trace references and classify live/version-specific/leftover/unused/reserved data.
