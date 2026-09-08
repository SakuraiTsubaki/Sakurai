# Address model

The workset records both Game Boy CPU addresses and absolute ROM file offsets.

## ROM

- Bank 00 CPU `$0000-$3FFF` → file offsets `0x00000-0x03FFF`.
- Switchable Bank `N > 0` CPU `$4000-$7FFF` → file offset `N * 0x4000 + (CPU - 0x4000)`.
- The 512 KiB cartridge therefore occupies file offsets `0x00000-0x7FFFF` across banks `00-1F`.

`tools/parse_rgbds_symbols.py` applies this conversion to every ROM symbol and section emitted by RGBDS. Non-ROM domains (VRAM, SRAM, WRAM, HRAM, I/O/OAM) retain their CPU addresses and bank metadata but deliberately have no ROM file offset.

## Why both representations are stored

CPU addresses describe execution and pointer windows; absolute offsets identify bytes in the canonical `.gb` input. Keeping both makes a symbol or section directly joinable to page hashes, bank hashes, and revision diff runs without losing Game Boy banking semantics.
