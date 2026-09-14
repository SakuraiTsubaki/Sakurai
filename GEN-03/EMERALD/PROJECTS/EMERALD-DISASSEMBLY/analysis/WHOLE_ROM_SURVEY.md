# Whole-ROM Survey — Initial 64 KiB Pass

This is the first coarse same-offset comparison across the six unique reference releases: JPN, ENG, FRA, DEU, ITA and ESP. The duplicate English `(U)` file is omitted because it is byte-identical to the `(USA, Europe)` file.

## Method

The 16 MiB address space was divided into 256 blocks of 64 KiB (`0x10000`). Each block was SHA-1 hashed independently for every release. `whole_rom_64k_map.csv` records which releases have identical payloads at the same offset.

This pass is a locator, not a semantic map. Localization changes can shift later data and pointer layouts, so a different same-offset hash does not mean an entire 64 KiB block is conceptually different.

## Results

- 256 total 64 KiB blocks
- 36 blocks are identical across all six unique releases: 2,359,296 bytes, or 14.06% of the ROM address space
- 32 blocks split cleanly into `JPN` versus a byte-identical `ENG+FRA+DEU+ITA+ESP` group
- 186 blocks have six distinct same-offset payloads
- one block at `0x009D0000-0x009DFFFF` forms three groups: `JPN`, `DEU`, and `ENG+FRA+ITA+ESP`
- one block at `0x00DA0000-0x00DAFFFF` forms five groups, with only `DEU+ITA` identical

Large all-version-identical runs at this granularity:

- `0x00B00000-0x00B8FFFF` (576 KiB)
- `0x00E00000-0x00E2FFFF` (192 KiB)
- `0x00E40000-0x00EFFFFF` (768 KiB)
- `0x00F40000-0x00FFFFFF` (768 KiB)

Several of the high-address identical runs are likely shared payload and/or padding/filler and must be classified before being treated as meaningful assets.

## Next pass

1. classify filler/padding separately from meaningful shared data
2. reduce block size in transition regions
3. identify pointers, code ranges and compressed-data signatures
4. correlate discovered ranges with known Emerald structures
5. begin semantic extraction into `src/`, `asm/`, `data/`, `graphics/`, `text/`, `sound/` and `maps/`
