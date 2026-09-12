# RBY Title Logo Correction v0.2

## Correction

The first prototype was wrong. It assumed that the Japanese and English Red ROMs stored the title logo at the same file offset (`0x10419`).

They do not.

- Japanese Red/Green target logo: file offset `0x10419`
- English Red `PokemonLogoGraphics`: ROM address `04:5380`, file offset `0x11380`
- Asset size: `0x700` bytes = 112 Game Boy 2bpp tiles = 16 × 7 tiles

The v0.1 English source block was unrelated data, which is why the displayed logo was corrupted.

## v0.2

The verified English Pokémon logo is copied from English Red file offset `0x11380` into each Japanese Red/Green ROM's title-logo block at `0x10419`.

The Japanese ROM remains the base. Version-specific Red/Green title data remains intact.

Corrected:
- Red Rev 0
- Red Rev A
- Green Rev 0
- Green Rev A

Each IPS was applied back to a clean source ROM and reproduced the corrected ROM byte-for-byte.

**v0.1 artifacts must not be used.**
