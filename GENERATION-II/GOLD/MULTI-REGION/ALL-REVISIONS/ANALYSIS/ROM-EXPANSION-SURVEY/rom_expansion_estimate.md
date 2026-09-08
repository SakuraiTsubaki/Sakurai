# Pokémon Gold multi-region ROM expansion survey

Date: 2026-09-08

## Scope
Survey all uploaded Pokémon Gold regional/revision ROMs and estimate ROM expansion needed to host Generation II-era content plus later-generation core content in a single GBC-style project. Original ROMs are read-only and are not included in this package.

## Verified source-ROM facts
- Japan v1.0: 1 MiB / 64 × 16 KiB banks / MBC3+RTC / header ROM size code 0x05.
- Japan Rev A: 1 MiB / 64 banks / MBC3+RTC / header ROM size code 0x05.
- Korea, USA/Europe, Spain, Germany, France, Italy: 2 MiB / 128 banks / MBC3+RTC / header ROM size code 0x06.
- All uploaded ROMs use cartridge type 0x10 (MBC3 + Timer + RAM + Battery).
- Korean ROM has 24 completely uniform 00/FF 16-KiB banks = 384 KiB of immediately obvious bank-sized slack.
- USA/Europe ROM has 28 completely uniform 16-KiB banks = 448 KiB of immediately obvious bank-sized slack.
- The broader long-run scan finds ~0.86 MiB (Korea) and ~0.90 MiB (USA/Europe) of 00/FF runs >=256 bytes, but this is only a candidate-space metric and must not be treated as proven free space without pointer/reachability analysis.
- Japanese 1 MiB builds are packed far more tightly: no fully blank 16-KiB bank was found; only ~20 KiB of long 00/FF runs >=256 bytes.

## Mapper limits
- MBC3: 2 MiB ROM maximum (128 banks), so the existing 2 MiB localized builds are already at the mapper's nominal ROM-addressing ceiling.
- MBC30-style extension: 4 MiB ROM can preserve MBC3-style RTC behavior, but is non-standard for Gold and requires mapper/bank-switching compatibility work.
- MBC5: 8 MiB ROM maximum (512 banks), but standard MBC5 does not provide the MBC3 RTC, so RTC must be replaced/emulated or a custom mapper/flashcart target used.

## Recommended capacity tiers
### 4 MiB — minimum engineering target
Adds 2 MiB / 128 banks over a 2 MiB Gold base. Enough for a substantial modernized engine and many later-generation species/moves/forms if graphics, text, animations, and world content are aggressively curated/compressed. Not a comfortable target for literally all later content.

### 8 MiB — recommended single-ROM target
Adds 6 MiB / 384 banks over a 2 MiB Gold base (or 7 MiB / 448 banks over Japanese 1 MiB builds). This is the practical ceiling of standard MBC5 and provides enough headroom for 16-bit species/move/item IDs, roughly 1,000+ species plus forms, modern battle tables, GBC-style sprites/icons, descriptions, and substantial future Generation X headroom—provided later assets are converted to GBC formats and the project does not attempt to preserve every later region/story/map verbatim.

### 16–32 MiB — only for “literally everything”
If “all later content” includes every region, map, NPC/event, story, music set, battle facility, and multiple language text packs, 8 MiB stops being a safe ceiling. A 16–32 MiB custom mapper/flashcart/emulator format or a multi-ROM architecture is more realistic. This is no longer a stock cartridge-compatible Gold expansion.

## Structural expansion required regardless of ROM size
- 8-bit Pokémon species IDs -> 16-bit.
- 8-bit move IDs -> 16-bit.
- 8-bit item IDs -> 16-bit (or separate 16-bit namespaces).
- Save/party/box/Pokédex structures must be redesigned for >255 species and modern form data.
- Far pointers and bank-aware tables must be generalized beyond original assumptions.
- Battle engine must gain later mechanics as desired: abilities, natures, physical/special split, Fairy, newer status/weather/terrain rules, form changes, modern evolution methods, etc.
- Graphics loaders and sprite-pointer tables must support many more banks/assets.
- If ROM exceeds 2 MiB, MBC3 banking cannot address it without changing mapper behavior.

## Capacity recommendation
For a Gold-based “everything from Gen II through later generations” engine, design for 8 MiB from the start, with 16-bit IDs and a bank abstraction that does not hard-code 7-bit MBC3 banks. Reserve an optional 16 MiB custom-mapper profile if the scope grows to include full later regions/stories or simultaneous multi-language resources.
