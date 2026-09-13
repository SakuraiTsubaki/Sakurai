# Pokémon Yellow / Pikachu — Full Disassembly Stage 0 Status

## Scope

- Uploaded filenames: 14
- Unique ROM SHA-1s: 9
- Banks per ROM: 64 (`00`–`3F`)
- Bank size: 16 KiB
- Unique banks processed: 576
- Exact-source rebuild verification: **9/9 PASS**

## What Stage 0 means

Every byte of every unique ROM was emitted to bank-separated RGBDS-style `db` source. Each emitted byte sequence has an LR35902 linear-decode comment. The generated sources were parsed back into raw bytes and SHA-1 checked against the corresponding uploaded ROM. This gives a byte-complete, lossless disassembly scaffold without falsely treating text/graphics/audio as executable code.

The exact ASM blobs are intentionally kept in the local work package rather than committed here. This repository stores reproducible analysis, mappings, and tooling; the uploaded ROMs remain the local source of truth.

## Canonical semantic reference

The English unique ROM SHA-1 is `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`, exactly matching the canonical pret/pokeyellow build. Its `layout.link` therefore provides a reliable semantic bank map for the English ROM.

## Exact bank identity anchors

- All 9 unique ROMs identical: `1B`, `32`
- All 4 Japanese revisions identical: `19`, `1B`, `32`
- All 5 international releases identical: `0C`, `1A`, `1B`, `21`, `22`, `23`, `24`, `25`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`
- JP Rev D and EN identical: `0C`, `1B`, `21`, `22`, `23`, `24`, `25`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `39`
- EN and IT additionally share `1F` while FR/DE/ES differ there.

## High-level canonical EN bank roles

- `00`: vectors/header/Home
- `01`: title, menus, overworld, naming, marts/centers, Pokédex display
- `02`, `08`, `1F`, `20`: audio engines/music/SFX
- `04`–`05`, `09`–`0D`, `13`, `19`–`1B`, `39`: graphics-heavy/mixed
- `06`–`07`, `11`–`18`, `1D`: maps/events-heavy
- `0E`–`0F`, `3D`: battle engine/core
- `21`–`25`, `31`–`38`: Pikachu cries
- `26`–`2D`: main text banks
- `2E`: Pokédex text
- `2F`: move names + CGB BG attributes
- `30`: canonical EN garbage bank
- `3A`: Pokémon names + printer/NPC movement
- `3B`: canonical EN empty
- `3C`: Pikachu PCM + maps/credits/events
- `3E`: Surfing Pikachu / intro / animated objects
- `3F`: overworld Pikachu systems

## Revision/language changed-byte totals

- JP Rev 0A → B: 307,668 bytes
- JP Rev B → C: 39,485 bytes
- JP Rev C → D: 245,538 bytes
- JP Rev D → EN: 507,517 bytes
- EN → FR: 329,172 bytes
- EN → DE: 315,913 bytes
- EN → IT: 319,832 bytes
- EN → ES: 323,307 bytes

These totals include relocation effects and should not be read as semantic-change counts.

## Anchor mapping

A second pass finds exact matching blocks of at least 32 bytes even when their offsets moved. Total anchored bytes:

- JP0A→JPB: 717,128
- JPB→JPC: 809,695
- JPC→JPD: 777,819
- JPD→EN: 575,888
- EN→FR: 703,798
- EN→DE: 705,943
- EN→IT: 711,979
- EN→ES: 706,438

For JPD→EN, text-localization banks `26`–`30` (and `3B`) are the hardest semantic mapping region, while many graphics/audio banks remain almost completely anchorable.

## Next semantic pass

Convert Stage 0 to a real symbolic RGBDS disassembly bank-by-bank:

1. `00` Home/vectors/header and bank-switch core
2. code-heavy `01`, `03`, `0E`, `0F`, `10`, `1C`, `3D`, `3E`, `3F`
3. map/event banks
4. graphics/audio banks
5. text `26`–`2F`, Pokémon names `3A`
6. garbage/empty/padding classification (`30`, `3B`)

For every converted region: assign labels, identify pointer tables and cross-bank callers, preserve variant-specific differences, and verify lossless rebuild after each bank.
