# GBA Header Analysis

Reference range: `0x000000-0x0000BF` (192 bytes)

All nine initial Sapphire references were compared byte-for-byte across the complete GBA header range.

## Result

Only **four byte offsets differ** across the nine headers:

| Offset | Meaning | Observed values |
| ---: | --- | --- |
| `0x000` | First byte of ARM entry branch | `0x32` or `0x7F` |
| `0x0AF` | Region/language byte of game code | `J`, `E`, `D`, `F`, `I` |
| `0x0BC` | Software version | `0`, `1`, `2` |
| `0x0BD` | Header complement checksum | target-dependent |

The remaining **188 of 192 header bytes are identical** across the initial reference set.

## Entry branch

The four entry bytes are one of:

```text
32 00 00 EA   ; ARM B with immediate 0x32 -> target 0x000000D0
7F 00 00 EA   ; ARM B with immediate 0x7F -> target 0x00000204
```

Observed grouping:

- `0x000000D0`: Japanese `AXPJ` and English/European `AXPE` targets
- `0x00000204`: German `AXPD`, French `AXPF`, and Italian `AXPI` targets

This split must be represented by target-aware startup/linker source rather than hidden in a base ROM.

## Target matrix

| Target | Game code | SW ver. | Entry target | Header checksum |
| --- | --- | ---: | ---: | ---: |
| `JPN-AXPJ-v0` | `AXPJ` | 0 | `0xD0` | `0x50` |
| `USA-AXPE-v0` | `AXPE` | 0 | `0xD0` | `0x55` |
| `EUR-AXPE-v1` | `AXPE` | 1 | `0xD0` | `0x54` |
| `USA-EUR-AXPE-v2` | `AXPE` | 2 | `0xD0` | `0x53` |
| `DEU-AXPD-v1` | `AXPD` | 1 | `0x204` | `0x55` |
| `FRA-AXPF-v0` | `AXPF` | 0 | `0x204` | `0x54` |
| `FRA-AXPF-v1` | `AXPF` | 1 | `0x204` | `0x53` |
| `ITA-AXPI-v0` | `AXPI` | 0 | `0x204` | `0x51` |
| `ITA-AXPI-v1` | `AXPI` | 1 | `0x204` | `0x50` |

## Checksum verification

For every reference ROM, the stored byte at `0x0BD` matches the standard GBA complement checksum calculated over `0x0A0-0x0BC`:

```text
checksum = (-sum(header[0xA0:0xBD]) - 0x19) & 0xFF
```

All nine: **PASS**.

## Reconstruction status

- `[x]` Header range identified
- `[x]` Cross-version differences mapped
- `[x]` Entry branch targets identified
- `[x]` Header checksums independently verified
- `[ ]` Header emitted from assembly/build configuration
- `[ ]` Startup code at `0xD0` / `0x204` disassembled and labeled
- `[ ]` Header bytes reproduced by target builds
