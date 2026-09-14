# Startup reconstruction analysis

This document records the first executable-region reconstruction across the nine Pokémon Sapphire reference ROMs.

## Entry-point families

The first ARM instruction at file offset `0x000000` is an unconditional branch to `Init`.

| Target family | Game code(s) | `Init` file offset | Runtime address | Extended metadata at `0xD0` |
| --- | --- | ---: | ---: | --- |
| Japanese | `AXPJ` | `0xD0` | `0x080000D0` | no |
| English / English-European | `AXPE` | `0xD0` | `0x080000D0` | no |
| German | `AXPD` | `0x204` | `0x08000204` | yes |
| French | `AXPF` | `0x204` | `0x08000204` | yes |
| Italian | `AXPI` | `0x204` | `0x08000204` | yes |

The ARM startup instruction body from `Init` through the end of `IntrMain` is structurally identical in all nine analyzed ROMs.

- instruction bytes before the literal pool: `0x170` bytes
- common bytes including the `INTR_VECTOR` literal: `0x174` bytes
- reconstructed startup block including target literals: `0x17C` bytes
- common instruction-prefix SHA-256: `daee9bf5ae357010449d35a063863ff7cc328d9e52126ddb0b1debc3ec0c718c`

The first target-dependent values are literal-pool addresses rather than different startup logic.

## Startup literals

| Target | `INTR_VECTOR` | `AgbMain` pointer | `gIntrTable` pointer |
| --- | ---: | ---: | ---: |
| `JPN-AXPJ-v0` | `0x03007FFC` | `0x0800024D` | `0x03001B30` |
| `USA-AXPE-v0` | `0x03007FFC` | `0x0800024D` | `0x03001BC0` |
| `EUR-AXPE-v1` | `0x03007FFC` | `0x0800024D` | `0x03001BC0` |
| `USA-EUR-AXPE-v2` | `0x03007FFC` | `0x0800024D` | `0x03001BC0` |
| `DEU-AXPD-v1` | `0x03007FFC` | `0x08000381` | `0x03001BC0` |
| `FRA-AXPF-v0` | `0x03007FFC` | `0x08000381` | `0x03001BC0` |
| `FRA-AXPF-v1` | `0x03007FFC` | `0x08000381` | `0x03001BC0` |
| `ITA-AXPI-v0` | `0x03007FFC` | `0x08000381` | `0x03001BC0` |
| `ITA-AXPI-v1` | `0x03007FFC` | `0x08000381` | `0x03001BC0` |

`AgbMain` is a Thumb entry (`bit 0 = 1`). The actual first Thumb instruction is therefore at `0x0800024C` for `AXPJ/AXPE` and `0x08000380` for `AXPD/AXPF/AXPI`.

## Extended localization metadata (`0xD0–0x203`)

German, French, and Italian ROMs contain a `0x134`-byte metadata block between the normal GBA header/GPIO area and `Init`. This is why their header branch targets `0x204` instead of `0xD0`.

The block layout observed in all three languages is:

| Relative offset | Size | Meaning / current interpretation |
| --- | ---: | --- |
| `0x00` | `0x30` | twelve `0xFFFFFFFF` words |
| `0x30` | `4` | game version (`1` for Sapphire) |
| `0x34` | `4` | language ID (`3` French, `4` Italian, `5` German) |
| `0x38` | `0x18` | ASCII `pokemon sapphire version` |
| `0x50` | `8` | zero padding |
| `0x58` | `0x28` | ten ROM pointers to graphics/name/decoration tables |
| `0x80` | `0xB0` | fixed constants / reserved data |
| `0x130` | `4` | terminating `0xFFFFFFFF` |

The French Rev 0 and Rev 1 blocks are byte-identical. The Italian Rev 0 and Rev 1 blocks are also byte-identical. Only German Rev 1 is present in the current reference set.

Reconstructed sources live in:

- `data/localization_metadata.inc`
- `data/localization/de.s`
- `data/localization/fr.s`
- `data/localization/it.s`

Each locale source has been independently assembled and compared against the corresponding retail block; all `308` bytes match exactly.

## Byte-identical startup source

`src/startup.s` reconstructs `Init`, `IntrMain`, the stack literals, and the startup literal pool. It was assembled as ARMv4T with target-specific literal overrides and compared against every reference ROM.

**Result: 9/9 reference ROMs reproduce the complete `0x17C`-byte startup block exactly.**

Target-specific assembler values are limited to:

- Japanese: `G_INTR_TABLE_PTR=0x03001B30`
- German/French/Italian: `AGB_MAIN_PTR=0x08000381`
- AXPE targets use the source defaults (`0x0800024D`, `0x03001BC0`)

The next executable reconstruction boundary is `AgbMain` in Thumb code, followed by function-by-function mapping of early boot initialization.

## External cross-check

The reconstructed control flow agrees with the public `pret/pokeruby` `src/crt0.s` layout for `Init`/`IntrMain`. The multi-language comparison here additionally confirms that the extended pre-`Init` metadata layout used by the German build also exists in the analyzed French and Italian Sapphire ROMs.
