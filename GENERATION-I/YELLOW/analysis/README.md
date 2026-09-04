# Pokémon Yellow ROM census

Generated from the 14 project ROM files. ROM binaries are **not** stored in GitHub; identification is by cryptographic hashes and header metadata only.

## Summary

- Files inspected: **14**
- Binary-unique ROM images: **9**
- Languages: **JP / EN / DE / FR / IT / ES**
- Japanese revisions: **Rev 0A / B / C / D**
- EN/DE/FR/IT/ES each appear twice under `.gb` and `.gbc` filenames, but each pair is byte-for-byte identical.
- Every image is **1,048,576 bytes = 1 MiB = 64 × 16 KiB banks**.
- All 14 images pass both the Game Boy header checksum and global checksum calculations.

## Unique binaries

| Lang | Revision | SHA-1 | MD5 | Cart | CGB mode | Copies |
|---|---|---|---|---|---|---:|
| JP | Rev 0A | `1fb6c264e950d97ce3fd99b347e485b2150df4ff` | `aa13e886a47fd473da63b7d5ddf2828d` | 0x13 MBC3+RAM+BATTERY | DMG/SGB | 1 |
| JP | Rev B | `28e4b8531ea4ea1de5a396fccb0cfba51b06b149` | `96c1f411671b6e1761cf31884dde0dbb` | 0x13 MBC3+RAM+BATTERY | DMG/SGB | 1 |
| JP | Rev C | `91864ecdf26d1c593bde4d9ed615520eb57d5e41` | `5d9c071cf6eb5f3a697bbcd9311b4d04` | 0x13 MBC3+RAM+BATTERY | DMG/SGB | 1 |
| JP | Rev D | `a40298a8123613ee60cd7aab204d788b8425976e` | `90ae2ea218f8e21afa678c6a4e7b6013` | 0x13 MBC3+RAM+BATTERY | DMG/SGB | 1 |
| EN | Rev 0 | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` | `d9290db87b1f0a23b89f99ee4469e34b` | 0x1B MBC5+RAM+BATTERY | CGB-compatible | 2 |
| DE | Rev 0 | `42f3714eec6eca25200d42461ff08d57c98f6d1d` | `e93f10168e3c9b9d18e3ad4a1415e1d0` | 0x1B MBC5+RAM+BATTERY | CGB-compatible | 2 |
| FR | Rev 0 | `0aceec0ef7aa2ca5aa831554598d91f61a925591` | `2df6b439a35e0d511d52fa75c6a7849a` | 0x1B MBC5+RAM+BATTERY | CGB-compatible | 2 |
| IT | Rev 0 | `05bb8e99f24d498613930949730afa8024e77d08` | `3343ceca5dd6586e4774609526167d55` | 0x1B MBC5+RAM+BATTERY | CGB-compatible | 2 |
| ES | Rev 0 | `1dc242039218fba50928d1afb66b70565b6b9daf` | `f0da8b1cff3aab898ecde9dcbda6d817` | 0x1B MBC5+RAM+BATTERY | CGB-compatible | 2 |

## Duplicate filename pairs

- **IT** — same SHA-1 `05bb8e99f24d498613930949730afa8024e77d08`:
  - `Pokemon - Versione Gialla - Speciale Edizione Pikachu (Italy) (GBC,SGB Enhanced).gb`
  - `Pokemon - Versione Gialla (Italy).gbc`
- **FR** — same SHA-1 `0aceec0ef7aa2ca5aa831554598d91f61a925591`:
  - `Pokemon - Version Jaune (France).gbc`
  - `Pokemon - Version Jaune - Edition Speciale Pikachu (France) (GBC,SGB Enhanced).gb`
- **ES** — same SHA-1 `1dc242039218fba50928d1afb66b70565b6b9daf`:
  - `Pokemon - Edicion Amarilla - Edicion Especial Pikachu (Spain) (GBC,SGB Enhanced).gb`
  - `Pokemon - Edicion Amarilla (Spain).gbc`
- **DE** — same SHA-1 `42f3714eec6eca25200d42461ff08d57c98f6d1d`:
  - `Pokemon - Gelbe Edition (Germany).gbc`
  - `Pokemon - Gelbe Edition - Special Pikachu Edition (Germany) (GBC,SGB Enhanced).gb`
- **EN** — same SHA-1 `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1`:
  - `Pokemon - Yellow Version (USA, Europe).gbc`
  - `Pokemon - Yellow Version - Special Pikachu Edition (USA, Europe) (GBC,SGB Enhanced).gb`

## Header-level split

- **JP Rev 0A/B/C/D**: CGB flag `0x00`, SGB flag `0x03`, cartridge `0x13` = MBC3+RAM+BATTERY, destination `0x00`.
- **EN/DE/FR/IT/ES**: CGB flag `0x80` (CGB-compatible), SGB flag `0x03`, cartridge `0x1B` = MBC5+RAM+BATTERY, destination `0x01`.
- Header version bytes for JP are `0,1,2,3` respectively; all five international binaries use version `0`.

## Project handling rule

- Never commit original ROM binaries to GitHub.
- Commit analysis reports, inventories, scripts, tables, patches, test vectors, and other non-ROM outputs.
- Use SHA-1/SHA-256 to bind every derived result to an exact source ROM.

## Next census layer

Bank-by-bank hashes and byte-difference maps should be generated next for: JP revision lineage, EN↔DE↔FR↔IT↔ES localization structure, and JP↔international engine/layout changes.
