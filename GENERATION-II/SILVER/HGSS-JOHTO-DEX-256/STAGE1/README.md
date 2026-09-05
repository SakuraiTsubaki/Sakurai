# SILVER — HGSS Johto Pokédex 256 / Stage 1

## Goal
Expand all eight Pokémon Silver ROM targets from the vanilla 251-species model to the HGSS Johto Pokédex's 256-species roster, while preserving each Silver version's language/content identity.

## Canonical 16-bit species IDs
Vanilla species retain logical IDs `1..251`. The five HGSS Johto additions receive new logical IDs:

| Logical ID | National Dex | Species | HGSS Johto # | Evolution trigger |
|---:|---:|---|---:|---|
| 252 | 469 | Yanmega | 102 | Yanma level-up while knowing AncientPower (#246) |
| 253 | 424 | Ambipom | 124 | Aipom level-up while knowing Double Hit (new logical move #252) |
| 254 | 463 | Lickilicky | 181 | Lickitung level-up while knowing Rollout (#205) |
| 255 | 465 | Tangrowth | 183 | Tangela level-up while knowing AncientPower (#246) |
| 256 | 473 | Mamoswine | 197 | Piloswine level-up while knowing AncientPower (#246) |

The final Pokédex positions remain Lugia #252, Ho-Oh #253, Mewtwo #254, Mew #255, Celebi #256.

## HGSS-native base parameters staged for the five additions
Stat order in the binary base record is `HP, Atk, Def, Spe, SpA, SpD`.

| Species | Stats | Type | Catch | Gen-IV base EXP | Growth | Egg group |
|---|---|---|---:|---:|---|---|
| Yanmega | 86/76/86/95/116/56 | Bug/Flying | 30 | 198 | Medium Fast | Bug |
| Ambipom | 75/100/66/115/60/66 | Normal | 45 | 186 | Fast | Field |
| Lickilicky | 110/85/95/50/80/95 | Normal | 30 | 193 | Medium Fast | Monster |
| Tangrowth | 100/100/125/50/110/50 | Grass | 30 | 211 | Medium Fast | Grass |
| Mamoswine | 110/130/80/80/70/60 | Ice/Ground | 50 | 207 | Slow | Field |

Double Hit is staged as a new logical move #252 with Gen-IV parameters: Normal, 35 power per hit, 90% accuracy, 10 PP, exactly 2 hits.

## ROM census findings used by the patch
- All eight ROMs contain the same 251-entry New Pokédex order as a complete permutation of species IDs 1..251.
- All eight ROMs contain byte-identical `251 × 32-byte` Silver base-data tables (SHA-256 `dccd0f065a1ccba8ee1a1b7dbee960574499262a2739f46f67fa2f7e686654ac`).
- The international/Korean 2 MiB ROMs have Bank `$7E` entirely zero-filled.
- Japanese Rev0/RevA are 1 MiB. Stage 1 expands them to 2 MiB (MBC3 maximum), changes header ROM-size code `$05 → $06`, and uses the same Bank `$7E` as the other versions.

## Stage-1 payload layout
The payload starts at file offset `$1F8000` (ROM Bank `$7E`) and is 9,584 bytes.

- 64-byte `SJ256P1` header + CRC32
- 256 × 16-bit logical-species → National-Dex map
- 256 × 16-bit HGSS Johto order
- 256 × 33-byte 16-bit base-data records
- five evolution-by-known-move metadata records
- one Double Hit metadata record

For species 1..251, the new 33-byte base record is the original 32-byte Silver record with the leading one-byte species index widened to 16 bits. For the five additions, Silver-safe ancillary fields are inherited from the direct predecessor while direct HGSS-equivalent parameters are replaced.

## Current status
**Data staging is complete, engine routing is not.** The generated `DATA-STAGED` ROMs still execute the vanilla one-byte species engine. They are intentionally not labeled as final/playable 256-species builds.

The next engine stage must port the 16-bit species-index conversion architecture into Gold/Silver and route at least:

- party/box/save species handling and reserved values
- base-data lookup
- Pokémon names and named-object lookup
- evolution/level-up learnset lookup
- front/back sprite, palette, icon and cry lookup
- Pokédex order, caught/seen flags and dex display
- wild encounters, trainer parties, trades and daycare/breeding
- Hall of Fame and special event species storage
- link/time-capsule handling for extended species
- `EVOLVE_MOVE_KNOWN`
- Double Hit move data/effect/animation hookup

The reference architecture is the stable `expand-mon-ID` branch of `fellowship-of-the-roms/pokecrystal16`, ported to the Silver engine rather than copying Crystal content.

## Files
- `manifest.json` — canonical 256-species order and new-species parameters
- `build_report.json` — per-ROM source/output hashes and offsets
- `build_stage1_payload.py` — reproducible Stage-1 data injector
- `validate_stage1.py` — independent payload/header validator

ROM files themselves are intentionally not committed to GitHub.
