# Pokémon Black / White EUR — Semantic Census Phase 2 (corrected)

This report extends the physical/NitroFS/NARC census into semantic classification. No ROM bytes were modified.

## Coverage
- NARC archives classified: **237/237**
- Named/role-bearing archives with confirmed/high/probable identification: **34**
- Remaining archives retain structural categories rather than invented names.
- BW1/BW2 path mappings are kept separate; B2W2-only mappings are not promoted into the BW1 ledger.

## Core confirmed/high-confidence resources

| Path | Role | Confidence | Members | Size pattern |
|---|---|---|---:|---|
| `/skb.narc` | Soft keyboard / text-entry UI resources | high | 6 | 552 / 14400.0 / 14400 B |
| `/soundstatus.narc` | Sound/status UI resources | high | 4 | 552 / 1636.0 / 8256 B |
| `/titledemo.narc` | Title/opening demo resources | confirmed | 20 | 320 / 1572.0 / 65584 B |
| `/a/0/0/2` | Message/system text bank | confirmed | 288 | 20 / 1432.0 / 252092 B |
| `/a/0/0/3` | Story/overworld text bank | confirmed | 472 | 32 / 868.0 / 160444 B |
| `/a/0/0/4` | Pokémon battle sprite/animation compound resources | high | 14285 | 0 / 349 / 6516 B |
| `/a/0/0/6` | Battle particle/effect resources (SPA) | high | 733 | 1196 / 9888 / 34988 B |
| `/a/0/0/7` | Pokémon menu icon resources | high | 1431 | 0 / 362 / 1072 B |
| `/a/0/0/8` | Map/model resources | confirmed | 649 | 480 / 25632 / 99520 B |
| `/a/0/1/1` | Battle background/UI 2D+3D resources | high | 222 | 103 / 2248.0 / 100084 B |
| `/a/0/1/2` | ZoneData map association table: 427 × 48 B | confirmed | 1 | 20496 / 20496 / 20496 B |
| `/a/0/1/6` | Pokémon personal/base-stat data | confirmed | 669 | 56 / 60 / 1300 B |
| `/a/0/1/7` | Experience growth tables | confirmed | 8 | 404 / 404.0 / 404 B |
| `/a/0/1/8` | Level-up learnsets | confirmed | 668 | 4 / 64.0 / 92 B |
| `/a/0/1/9` | Evolution data | confirmed | 668 | 42 / 42.0 / 42 B |
| `/a/0/2/0` | Base evolution / baby-species mapping | confirmed | 650 | 2 / 2.0 / 2 B |
| `/a/0/2/1` | Move parameter data | confirmed | 560 | 36 / 36.0 / 36 B |
| `/a/0/2/3` | NFTR font resources | confirmed | 8 | 90 / 2040.0 / 264360 B |
| `/a/0/2/4` | Item parameter data | confirmed | 627 | 36 / 36 / 36 B |
| `/a/0/2/5` | Item sprite resources | high | 1005 | 107 / 552 / 560 B |
| `/a/0/2/6` | Title-screen resources | confirmed | 15 | 112 / 552 / 13882 B |
| `/a/0/5/7` | Field/event script archive | confirmed | 899 | 4 / 16 / 33176 B |
| `/a/0/6/6` | Move animation scripts | confirmed | 601 | 64 / 620 / 4576 B |
| `/a/0/6/7` | Battle effect scripts / auxiliary battle animations | high | 98 | 68 / 314.0 / 5596 B |
| `/a/0/7/1` | Trainer front/VS sprite resources | probable | 39 | 142 / 362 / 28864 B |
| `/a/0/7/2` | Trainer/back sprite resources | high | 760 | 60 / 99.0 / 2160 B |
| `/a/0/9/2` | Trainer metadata (TRData) | confirmed | 616 | 16 / 20.0 / 20 B |
| `/a/0/9/3` | Trainer party data (TRPoke) | confirmed | 616 | 6 / 16.0 / 108 B |
| `/a/1/2/5` | Overworld/NPC/map event object data | confirmed | 428 | 4 / 176.0 / 2178 B |
| `/a/1/2/6` | Wild encounter tables | confirmed | 112 | 232 / 232.0 / 928 B |
| `/a/1/6/3` | In-game trade data | probable | 7 | 44 / 44 / 44 B |
| `/a/1/7/8` | Species-indexed seasonal/location availability table | probable | 649 | 249 / 249 / 249 B |
| `/a/2/0/5` | Starter-selection scene resources | confirmed | 40 | 99 / 552.0 / 98388 B |
| `/a/2/3/1` | Help/manual full-screen images | confirmed | 73 | 11653 / 14485 / 30624 B |

## Field subsystem linkage

- `a/0/1/2` is exactly **20,496 B = 427 × 48 B**, matching the BW ZoneData table documented as one record per map/overworld set.
- `a/1/2/5` contains **428 members** and is the BW overworld/NPC event-object archive; the extra member is retained as part of the ROM census rather than assumed away.
- `a/0/5/7` contains **899 members** and is the BW field/event script archive.
- Previous cross-version notes that mapped BW scripts to `a/0/5/6` were B2W2-specific and are explicitly rejected for BW1.

## Expansion-relevant fixed data tables

- `a/0/1/6` personal data: 669 members; **667 × 60 B**, one 56 B member and one 1300 B special member.
- `a/0/1/9` evolution data: **668 × 42 B**.
- `a/0/2/0` baby/base-evolution mapping: **650 × 2 B**.
- `a/0/2/1` move parameters: **560 × 36 B**.
- `a/0/2/4` item parameters: **627 × 36 B**.
- `a/0/9/2` trainer metadata: 616 members; **615 × 20 B** plus one 16 B member.
- `a/0/9/3` trainer parties: variable 6–108 B; size scales with party composition.
- `a/1/2/6` encounters: **100 × 232 B** plus **12 × 928 B** seasonal-expanded records.
- `a/1/7/8`: **649 × 249 B** species-indexed fixed records; Black/White differences occur in 26 members and repeat with 62-byte season blocks.

## Version delta reminder
Only five ordinary NARCs differ between Black and White: `a/0/2/6`, `a/0/8/6`, `a/1/2/6`, `a/1/7/8`, and `a/2/3/1`. Across their contents, 66 member pairs differ. ARM9 overlays have 180 true decompressed differences.

## Rule for future phases
Unknown/custom archives are not force-labeled. Resolve them by BW1-specific references, ARM9/overlay xrefs, script consumers, file-index tables, and render/decode tests before promoting confidence.
