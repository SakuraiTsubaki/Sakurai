# Pokémon Yellow ROM audit

This package contains only hashes, header metadata, bank hashes, and comparison summaries. No ROM bytes are redistributed.

## Inventory

- Uploaded files scanned: **14**
- Byte-unique ROM images: **9**
- Exact duplicate filename pairs/groups: **5**
- Japanese unique revisions: **4**
- International unique language builds: **5**

## Common hardware/header facts

- All images are 1,048,576 bytes (1 MiB / 64 × 16 KiB ROM banks).
- All declare 32 KiB external RAM.
- All have valid Nintendo logo, header checksum, and global checksum.
- All are Super Game Boy enhanced (`SGB flag = 0x03`).
- Japanese revisions are DMG/SGB (`CGB flag = 0x00`) and use cartridge type `0x13` (MBC3+RAM+BATTERY).
- International builds are CGB-compatible (`CGB flag = 0x80`) and use cartridge type `0x1B` (MBC5+RAM+BATTERY).

## Exact duplicate aliases

- `05bb8e99f24d498613930949730afa8024e77d08`
  - `Pokemon - Versione Gialla (Italy).gbc`
  - `Pokemon - Versione Gialla - Speciale Edizione Pikachu (Italy) (GBC,SGB Enhanced).gb`
- `0aceec0ef7aa2ca5aa831554598d91f61a925591`
  - `Pokemon - Version Jaune (France).gbc`
  - `Pokemon - Version Jaune - Edition Speciale Pikachu (France) (GBC,SGB Enhanced).gb`
- `1dc242039218fba50928d1afb66b70565b6b9daf`
  - `Pokemon - Edicion Amarilla (Spain).gbc`
  - `Pokemon - Edicion Amarilla - Edicion Especial Pikachu (Spain) (GBC,SGB Enhanced).gb`
- `42f3714eec6eca25200d42461ff08d57c98f6d1d`
  - `Pokemon - Gelbe Edition (Germany).gbc`
  - `Pokemon - Gelbe Edition - Special Pikachu Edition (Germany) (GBC,SGB Enhanced).gb`
- `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`
  - `Pokemon - Yellow Version (USA, Europe).gbc`
  - `Pokemon - Yellow Version - Special Pikachu Edition (USA, Europe) (GBC,SGB Enhanced).gb`

## Japanese revision identity

- header version 0: `Pocket Monsters - Pikachu (Japan) (Rev 0A) (SGB Enhanced).gb` — SHA-1 `1fb6c264e950d97ce3fd99b347e485b2150df4ff`
- header version 1: `Pocket Monsters - Pikachu (Japan) (Rev B) (SGB Enhanced).gb` — SHA-1 `28e4b8531ea4ea1de5a396fccb0cfba51b06b149`
- header version 2: `Pocket Monsters - Pikachu (Japan) (Rev C) (SGB Enhanced).gb` — SHA-1 `91864ecdf26d1c593bde4d9ed615520eb57d5e41`
- header version 3: `Pocket Monsters - Pikachu (Japan) (Rev D) (SGB Enhanced).gb` — SHA-1 `a40298a8123613ee60cd7aab204d788b8425976e`

## Files

- `rom_manifest.csv` / `rom_manifest.json`: all 14 uploaded filenames and parsed header/checksum metadata.
- `unique_roms.json`: 9 byte-unique ROM images with alias lists.
- `duplicate_groups.json`: exact SHA-1 duplicate groups.
- `bank_sha1.csv`: SHA-1 for each 16 KiB bank of every unique image.
- `pairwise_diff_summary.csv`: byte-level and bank-level pairwise comparison of all 9 unique images.
- `inspect_yellow_roms.py`: standalone re-runnable inspector.

## Interpretation note

Filename extensions (`.gb` vs `.gbc`) are not evidence of different ROM content. The duplicate groups above are byte-identical, so one canonical image per SHA-1 is sufficient for analysis.
