# Pokémon Gold multi-region expansion capacity plan — 2026-09-08

## Scope
Eight uploaded Pokémon Gold ROMs were inspected directly: JP v1.0, JP Rev A, KR, EN/USA-Europe, FR, DE, ES, IT. Originals remain read-only.

## Direct ROM findings
- Japanese v1.0 and Rev A are 1 MiB / 64 banks.
- KR and all inspected Western localizations are 2 MiB / 128 banks.
- Cartridge type byte is 0x10 (MBC3 + TIMER + RAM + BATTERY) in all eight images.
- Full uniform blank 16 KiB bank counts: KR 24; EN 28; FR/DE/ES/IT 26 each; JP images 0.
- Full blank banks are only the easiest safe-space candidates; smaller 00/FF runs still require pointer/reference proof before reuse.
- JP v1.0 vs Rev A differs in 10,841 bytes across 10 banks; 10,821 changed bytes are concentrated in bank 0x23.

## Capacity recommendation
### Standard-hardware ceiling
8 MiB / 512 x 16 KiB banks is the practical standard Game Boy MBC5 ceiling. Moving from a 2 MiB Gold base therefore adds 6 MiB / 384 banks. MBC5 does not provide MBC3 RTC, so a real-cartridge build needs a custom RTC-capable MBC5-like mapper or an equivalent hardware solution.

### Recommended master architecture
Use a **16 MiB logical master layout / 1024 banks** for this project, even if an 8 MiB compatibility build is also produced. From a 2 MiB localized Gold base this is +14 MiB / +896 banks. This requires an extended/custom mapper or emulator/flash-cart support beyond standard MBC5.

Why 16 MiB: Gen X (Pokémon Winds/Waves, 2027) is announced but its full species/move/item roster is not public as of this report. Designing only for currently known counts would force another structural rewrite.

Reserve identifier spaces rather than current exact counts:
- Species IDs: 16-bit; reserve at least 2048 species.
- Form IDs: 16-bit and separate from species; reserve at least 4096 form records.
- Move IDs: 16-bit; reserve 2048.
- Item IDs: 16-bit; reserve 4096 (Gen IX item index space already exceeds 2048 in current games).
- Ability IDs: 16-bit; reserve 1024.
- Types: reserve 32 slots.

## 16 MiB bank budget
The accompanying CSV assigns all 1024 banks. Major allocations: 2 MiB original compatibility core, 0.75 MiB engine/bugfix migration, 3 MiB Pokémon graphics, 1.5 MiB moves/animations, 2 MiB Gen X/future reserve, plus data/text/audio/maps and 1.75 MiB slack.

## If 'everything' means every later region/story/map/music
16 MiB is for a Gold-centered game that incorporates later species/forms/moves/items/abilities/mechanics while retaining Johto/Kanto as the main world. If the requirement literally includes all later-generation regions, maps, scripts, trainers, facilities, music and story content, use a **32 MiB minimum planning target** and preferably a **64 MiB logical workspace**. That is no longer a standard MBC5 cartridge design; it is effectively a custom GBC engine/mapper project.

## Bug/glitch/error policy
Expansion and bug fixing must be one migration pass, not separate patches. Build a cross-version issue matrix with categories:
1. crash/corruption/security-like text interpreter issues;
2. save/RTC/storage integrity;
3. battle arithmetic and move/item logic;
4. map/event/script errors;
5. link/time-capsule synchronization;
6. localization-specific defects;
7. graphics/audio/UI defects;
8. design limitations that become bugs after 16-bit expansion.

Known examples to include in regression tests: Coin Case text terminator exploit (EN), Hall of Fame save initialization, Lucky Number box-loop limit, Fast/Love/Moon Ball logic, Dragon Fang/Dragon Scale effect mismatch, Present, Belly Drum, Beat Up link desync, Pursuit revival, stat rollover, daycare EXP loss, Bug-Catching Contest JP behavior, Dude tutorial language-specific defects, and map/event anomalies.

Every fix should receive: source/version, trigger, expected behavior, patched behavior, compatibility impact, automated regression test, and binary address/symbol mapping.

## Build targets
- `gold-modern-8m`: 8 MiB / 512 banks — standard MBC5-sized compatibility target; requires RTC strategy.
- `gold-modern-16m`: 16 MiB / 1024 banks — recommended full Gen X-ready master target; custom mapper.
- `gold-world-32m+`: only if all later regions/story/audio assets are included.
