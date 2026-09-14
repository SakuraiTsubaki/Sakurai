# Game Freak compatibility header (`0x000100-0x000203`)

The LeafGreen ROMs contain a `0x104`-byte compatibility/data-discovery header beginning at ROM offset `0x100`.

## Confirmed structure

| Relative offset | Size | Field |
|---:|---:|---|
| `0x00` | 4 | version |
| `0x04` | 4 | language |
| `0x08` | 32 | game name |
| `0x28` | 4 | Pokémon front-sprite table pointer |
| `0x2C` | 4 | Pokémon back-sprite table pointer |
| `0x30` | 4 | normal palette table pointer |
| `0x34` | 4 | shiny palette table pointer |
| `0x38` | 4 | icon table pointer |
| `0x3C` | 4 | icon palette-ID table pointer |
| `0x40` | 4 | icon palette table pointer |
| `0x44` | 4 | species-name table pointer |
| `0x48` | 4 | move-name table pointer |
| `0x4C` | 4 | decoration table pointer |
| `0x50` | 4 | SaveBlock1 flags offset |
| `0x54` | 4 | SaveBlock1 vars offset |
| `0x58` | 4 | SaveBlock2 Pokédex offset |
| `0x5C` | 4 | seen1 offset |
| `0x60` | 4 | seen2 offset |
| `0x64` | 4 | Pokédex var index |
| `0x68` | 4 | Pokédex flag |
| `0x6C` | 4 | Mystery Gift flag |
| `0x70` | 4 | National Dex count |
| `0x74-0x84` | 17 | name/string-length compatibility bytes |
| `0x88` | 4 | SaveBlock2 size |
| `0x8C` | 4 | SaveBlock1 size |
| `0x90-0xB4` | 40 | party/player/event save offsets |
| `0xB8` | 4 | zero/unknown field |
| `0xBC` | 4 | species info pointer |
| `0xC0` | 4 | ability-name table pointer |
| `0xC4` | 4 | ability-description pointer table |
| `0xC8` | 4 | item table pointer |
| `0xCC` | 4 | move/battle-move table pointer |
| `0xD0` | 4 | ball graphics table pointer |
| `0xD4` | 4 | ball palette table pointer |
| `0xD8` | 4 | GCN-link flags save offset |
| `0xDC` | 4 | game-clear flag |
| `0xE0` | 4 | ribbon flag |
| `0xE4-0xE9` | 6 | bag/PC capacity bytes |
| `0xEC` | 4 | PC items offset |
| `0xF0` | 4 | gift ribbons offset |
| `0xF4` | 4 | Enigma Berry offset |
| `0xF8` | 4 | Enigma Berry size |
| `0xFC` | 4 | move descriptions pointer (`0` in all seven targets) |
| `0x100` | 4 | terminal compatibility value (`0xFFFFFFFF`) |

## Cross-version invariants

The following values are identical in all seven analyzed ROMs:

- version: `5`
- game name: `pokemon green version`
- flags offset: `0x0EE0`
- vars offset: `0x1000`
- Pokédex offset: `0x18`
- seen1 offset: `0x05F8`
- seen2 offset: `0x3A18`
- Pokédex var index: `0x3C`
- Pokédex flag: `0x838`
- Mystery Gift flag: `0x839`
- Pokédex count: `0x182` (386)
- SaveBlock2 size: `0x0F24`
- party count offset: `0x34`
- party offset: `0x38`
- trainer ID offset: `0x0A`
- player name offset: `0x00`
- player gender offset: `0x08`
- external event flags offset: `0x30BB`
- external event data offset: `0x30A7`
- GCN-link flags offset: `0xA8`
- game-clear flag: `0x82C`
- ribbon flag: `0x83B`
- bag item/key item/Poké Ball/TM-HM/Berry capacities: `42/30/13/58/43`
- PC item capacity: `30`
- PC items offset: `0x298`
- gift ribbons offset: `0x309C`
- Enigma Berry offset/size: `0x30EC / 0x34`
- terminal value: `0xFFFFFFFF`

## Japanese-vs-international structural differences

The Japanese target is not merely a text swap. Its compatibility bytes encode shorter string limits in several positions, and its SaveBlock1 size differs:

- Japan SaveBlock1 size: `0x3D40`
- International SaveBlock1 size: `0x3D68`

Observed compatibility-byte sequence (`0x74-0x84`):

- Japan: `07 05 0A 05 07 08 06 07 04 0A 12 0A 0A 05 01 03 07`
- International: `07 0A 0A 0A 0C 0C 06 0C 06 10 12 0C 0F 0B 01 08 0C`

This difference must remain target-specific in the reconstruction.

## USA vs Europe Rev 1

For every non-null ROM pointer represented in this header, the Europe Rev 1 target is exactly `+0x70` relative to the USA target. The underlying logical tables therefore keep the same ordering while the later build has a 112-byte upstream layout shift.

This is a useful alignment anchor when building the revision-difference map.

## Source cross-check

The field interpretation was cross-checked against the public `pret/pokefirered` `GFRomHeader` reconstruction, while all values and offsets above were independently read from the seven uploaded LeafGreen ROM images.
