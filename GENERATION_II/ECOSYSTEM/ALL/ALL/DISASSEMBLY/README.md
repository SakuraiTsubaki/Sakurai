# Generation II Disassembly — Master Scope

This directory is the project-level control plane for the complete Pokémon Generation II disassembly effort. The canonical per-game source repositories remain:

- `SakuraiTsubaki/PocketMonsters-Kin-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Gin-Disassembly`
- `SakuraiTsubaki/PocketMonsters-Crystal-Disassembly`

## Scope rule

Generation II is treated as one complete technical generation, not as a short summary of Gold, Silver, and Crystal. Work is tracked across code, data, banks, pointers, maps, scripts, events, flags, battle logic, save/SRAM, communications, time/day/night, Pokégear/phone/radio, breeding, friendship, gender, held items, Pokémon, moves, items, trainers, NPCs, encounters, graphics, sprites, palettes, fonts, animation, audio, localization, UI, unused/debug material, bugs, revisions, regional/language variants, Generation I compatibility, and later-generation comparison.

## Baseline discipline

1. Gold, Silver, and Crystal are separate canonical reconstruction targets.
2. Gold/Silver revisions are never flattened into a single binary identity.
3. Crystal-only features are not backported into Gold/Silver descriptions.
4. Japanese, North American, European, and Korean retail data are tracked separately where they differ.
5. Korean Gold/Silver are treated as independent official technical targets for encoding/font/UI/localization analysis.
6. Generation I Time Capsule compatibility is a first-class cross-generation workstream.
7. Mobile System GB / Pokémon Communication Center and other region-specific services are tracked separately from ordinary offline Crystal behavior.
8. Unused/debug/development remnants are separated from retail-used content.
9. ROM binaries are never committed. Reconstructed source, metadata, tools, manifests, patches, and permissible extracted/recreated assets are tracked.
10. Every replacement of an INCBIN span with source must preserve an exact-match verification path for the relevant target.

## Active execution model

All major workstreams are active in parallel. Bank 00 is the first concrete source-reconstruction front in each core repository, while inventory work proceeds simultaneously across the rest of the ROM and ecosystem.

See `workstreams.json` for machine-readable project status.
