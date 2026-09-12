# Pokémon Emerald 64 KiB Bank Audit

## Scope

Audited the six unique Rev 0 Pokémon Emerald ROMs currently used by the project:

- JP / BPEJ
- EN / BPEE
- FR / BPEF
- DE / BPED
- IT / BPEI
- ES / BPES

The duplicate English `U` / `USA, Europe` files are treated as one unique BPEE ROM.

Analysis unit: `0x10000` bytes (64 KiB), banks `00` through `FF`.

ROM binaries are intentionally excluded from this repository.

## Global bank identity result

- All six ROMs byte-identical: **36 / 256 banks**
  - `B0-B8`
  - `E0-E2`
  - `E4-EF`
  - `F4-FF`
- All six ROMs distinct: **186 / 256 banks**
  - `00-9C`
  - `C1-D9`
  - `DB-DE`
- Overseas five identical, JP different: **32 banks**
  - `9E-AF`
  - `B9-C0`
  - `DF`
  - `E3`
  - `F0-F3`
- Special identity cases:
  - `9D`: EN+FR+IT+ES / DE / JP
  - `DA`: DE+IT / EN / ES / FR / JP

## Structural bank map

| Range | File offsets | Working classification |
|---|---:|---|
| `00-1D` | `000000-1DFFFF` | Main executable code |
| `1E-2C` | `1E0000-2CFFFF` | Event/script-data dominant |
| `2D` | `2D0000-2DFFFF` | Script-data tail → library code |
| `2E` | `2E0000-2EFFFF` | Runtime libraries: m4a, flash, RTC/RFU, BIOS wrappers, libgcc/libc |
| `2F-9C` overseas | `2F0000-9CFFFF` | Main read-only data, localized text, map/battle data, audio, multiboot aggregate |
| `92-AF` JP | `920000-AFFFFF` | JP padding/gap; overseas localization data continues into this area |
| `B0-B9` | `B00000-B9FFFF` | Animated Pokémon front-picture data |
| `BA-BF` | `BA0000-BFFFFF` | Padding/gap |
| `C0-DE` | `C00000-DEFFFF` | Main graphics data (`gfx_data`) |
| `DF-E2` | `DF0000-E2FFFF` | Padding/gap |
| `E3` | `E30000-E3FFFF` | Sparse residual/extra data; do not mark safe-free yet |
| `E4-EF` | `E40000-EFFFFF` | Common all-`FF` expansion-space candidate |
| `F0-F3` | `F00000-F3FFFF` | Region-dependent padding; JP contains sparse residue in `F3` |
| `F4-FF` | `F40000-FFFFFF` | Common all-`FF` expansion-space candidate |

## Source-backed boundaries

The public `pret/pokeemerald` linker script fixes the animated-mon front-picture section at ROM address `0x08B00000` and the main graphics section at `0x08C00000`. This exactly matches the observed `B0` and `C0` bank boundaries.

The `pret/pokeemerald-jp` US function map shows normal game functions through `0x081DB620`, followed by the next library-code region at `0x082DED70`. This supports the `1E-2C` script/data-dominant classification and the `2D` transition into library code.

References:

- https://github.com/pret/pokeemerald/blob/master/ld_script.ld
- https://github.com/pret/pokeemerald-jp/blob/master/funcmap_us.txt

## Pairwise byte-difference summary

| Pair | Exact 64 KiB banks | Different bytes |
|---|---:|---:|
| JP ↔ EN | 36/256 | 79.8132% |
| JP ↔ FR | 36/256 | 79.6489% |
| JP ↔ DE | 36/256 | 79.7915% |
| JP ↔ IT | 36/256 | 79.5879% |
| JP ↔ ES | 36/256 | 79.8387% |
| EN ↔ FR | 69/256 | 62.0436% |
| EN ↔ DE | 68/256 | 64.2848% |
| EN ↔ IT | 69/256 | 62.5526% |
| EN ↔ ES | 69/256 | 60.5486% |
| FR ↔ DE | 68/256 | 64.0167% |
| FR ↔ IT | 69/256 | 62.0058% |
| FR ↔ ES | 69/256 | 59.1709% |
| DE ↔ IT | 69/256 | 61.9864% |
| DE ↔ ES | 68/256 | 64.0423% |
| IT ↔ ES | 69/256 | 60.7961% |

## Expansion-space warning

Padding-looking banks are only candidates. Before any insertion, perform ROM-wide pointer/reference scans and check runtime-copy, multiboot, checksum, linker-placement, and region-specific dependencies. In particular, `E3` and JP `F3` are excluded from safe-free status at this stage.

## Next audit layer

The next pass should split every 64 KiB bank into concrete objects/tables using public symbol/linker maps and direct signature/pointer analysis, then create a bank-to-symbol ownership map for all six regional builds.
